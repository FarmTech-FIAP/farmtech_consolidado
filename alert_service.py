import os
import boto3
import numpy as np
from dotenv import load_dotenv
from sklearn.tree import DecisionTreeClassifier

# carrega as variaveis de ambiente
load_dotenv(override=True)

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")

# base de treino historica da fazenda para o modelo classificar o risco
# features: [umidade_solo, temperatura_dht]
dados_treino = np.array([
    [18.0, 32.0], [21.5, 30.5], [24.0, 35.0], [15.0, 33.0], [22.0, 29.0], # 0: seca/irrigacao urgente
    [42.0, 36.5], [45.0, 38.0], [50.0, 37.0], [38.0, 36.0], [40.0, 39.0], # 1: estresse termico
    [52.0, 24.0], [60.0, 25.5], [55.0, 23.0], [58.0, 26.0], [65.0, 22.0]  # 2: condicao normal
])

# rotulos das classes
classes_treino = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2])

# modelo de machine learning treinado na inicializacao
modelo_risco = DecisionTreeClassifier(random_state=42)
modelo_risco.fit(dados_treino, classes_treino)

# diagnosticos mapeados pelo resultado do modelo
DIAGNOSTICOS = {
    0: {
        "status": "Estresse Hídrico Crítico",
        "acao": "Acionamento imediato das bombas de irrigação do setor norte por 45 minutos.",
        "urgencia": "ALTA"
    },
    1: {
        "status": "Estresse Térmico Elevado",
        "acao": "Acompanhar taxa de evapotranspiração e programar turno de irrigação noturna.",
        "urgencia": "MÉDIA"
    },
    2: {
        "status": "Condição Agronômica Normal",
        "acao": "Manter monitoramento de rotina sem intervenção necessária.",
        "urgencia": "BAIXA"
    }
}

def diagnosticar_com_ia(umidade, temperatura):
    # entrada para predicao do modelo
    entrada = np.array([[float(umidade), float(temperatura)]])
    
    # inferencia do modelo treinado
    classe = int(modelo_risco.predict(entrada)[0])
    probabilidades = modelo_risco.predict_proba(entrada)[0]
    confianca = probabilidades[classe] * 100.0
    
    info = DIAGNOSTICOS[classe]
    
    assunto = f"Alerta FarmTech: {info['status']}"
    corpo = (
        f"DIAGNÓSTICO AUTOMÁTICO VIA MACHINE LEARNING:\n"
        f"Status Detectado: {info['status']}\n"
        f"Certeza do Modelo: {confianca:.1f}%\n"
        f"Leituras Analisadas: Umidade {umidade:.1f}% | Temperatura {temperatura:.1f}°C\n"
        f"Nível de Urgência: {info['urgencia']}\n"
        f"Ação Operacional Recomendada: {info['acao']}"
    )
    
    return assunto, corpo, info["status"], confianca

def enviar_alerta_aws(assunto, mensagem):
    # se faltar credenciais roda modo simulado
    if not SNS_TOPIC_ARN or not AWS_ACCESS_KEY_ID:
        return {
            "status": "simulado",
            "detalhes": f"[SIMULADO] {assunto}: {mensagem}"
        }

    try:
        sessao = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID.strip() if AWS_ACCESS_KEY_ID else None,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY.strip() if AWS_SECRET_ACCESS_KEY else None,
            aws_session_token=AWS_SESSION_TOKEN.strip() if AWS_SESSION_TOKEN else None,
            region_name=AWS_REGION.strip() if AWS_REGION else "us-east-1"
        )
        
        sns = sessao.client("sns")
        resposta = sns.publish(
            TopicArn=SNS_TOPIC_ARN.strip(),
            Subject=assunto,
            Message=mensagem
        )
        
        id_msg = resposta.get("MessageId", "")
        return {
            "status": "sucesso",
            "detalhes": f"Alerta enviado com sucesso via AWS SNS! ID: {id_msg}"
        }
    except Exception as e:
        return {
            "status": "erro",
            "detalhes": f"Falha ao enviar alerta: {str(e)}"
        }

# funcoes de apoio para os outros modulos do sistema continuarem funcionando
def checar_e_alertar_sensores(umidade, temperatura):
    assunto, corpo, _, _ = diagnosticar_com_ia(umidade, temperatura)
    return enviar_alerta_aws(assunto, corpo)

def checar_e_alertar_visao(objeto, confianca):
    if str(objeto).lower() == "vaca" and confianca > 0.60:
        msg = (
            f"AVISO DE SEGURANÇA:\n"
            f"Bovino detectado próximo à plantação (Confiança: {confianca*100:.1f}%).\n"
            f"Ação sugerida: Equipe de campo deve checar o cercamento do piquete 4."
        )
        return enviar_alerta_aws("Alerta FarmTech - Invasão de Bovino", msg)
    return {"status": "normal", "detalhes": "Sem anomalias visuais detectadas."}

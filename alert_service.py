import boto3
import os
from botocore.exceptions import NoCredentialsError

# No ambiente AWS Academy / Learner Lab, exporte as credenciais temporárias
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN", "")

def enviar_alerta_aws(assunto: str, mensagem: str, tipo="SIMULADO"):
    """
    Envia alertas aos operadores da fazenda usando AWS SNS.
    Se não houver credenciais ativas, gera log em modo de contingência/simulação.
    """
    if tipo == "SIMULADO" or not SNS_TOPIC_ARN:
        return {
            "status": "sucesso_simulado",
            "detalhes": f"[SIMULAÇÃO AWS SNS] Assunto: {assunto} | Mensagem: {mensagem}"
        }
    
    try:
        sns_client = boto3.client("sns", region_name=AWS_REGION)
        resposta = sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=assunto,
            Message=mensagem
        )
        return {"status": "sucesso_aws", "message_id": resposta.get("MessageId")}
    except Exception as e:
        return {"status": "erro", "detalhes": str(e)}

def checar_e_alertar_sensores(umidade: float, temperatura: float):
    """Regra de negócio: alerta se umidade do solo ou ar estiver crítica."""
    if umidade < 30.0:
        msg = (
            f"ALERTA CRÍTICO: Umidade em nível baixo ({umidade}%).\n"
            f"Ação corretiva recomendada: Ativar bombas do setor 2 por 45 minutos."
        )
        return enviar_alerta_aws("Alerta FarmTech: Irrigação Necessária", msg)
    elif temperatura > 35.0:
        msg = (
            f"AVISO TÉRMICO: Temperatura elevada detectada ({temperatura}°C).\n"
            f"Ação corretiva recomendada: Monitorar taxa de evapotranspiração da lavoura."
        )
        return enviar_alerta_aws("Alerta FarmTech: Calor Excessivo", msg)
    return {"status": "normal", "detalhes": "Parâmetros de solo e clima dentro da normalidade."}

def checar_e_alertar_visao(classe_detectada: str, confianca: float):
    """Regra de negócio: alerta de invasão de gado ou maquinário."""
    if classe_detectada.lower() == "vaca" and confianca > 0.60:
        msg = (
            f"AVISO DE SEGURANÇA: Bovino detectado próximo à área de plantio "
            f"(Confiança: {confianca*100:.1f}%).\n"
            f"Ação corretiva recomendada: Acionar contenção e checar cercamento do piquete 4."
        )
        return enviar_alerta_aws("Alerta FarmTech: Bovino Detectado", msg)
    return {"status": "normal", "detalhes": "Nenhuma anomalia de visão detectada."}

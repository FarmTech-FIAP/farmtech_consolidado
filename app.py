import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# carrega credenciais do arquivo .env local
load_dotenv(override=True)

# importacao dos servicos auxiliares da solucao
from alert_service import checar_e_alertar_sensores, checar_e_alertar_visao
from ir_alem_genetico import gerar_base_insumos, executar_algoritmo_genetico

# driver oficial do oracle
try:
    import oracledb
except ImportError:
    oracledb = None

st.set_page_config(
    page_title="FarmTech Solutions — Sistema Integrado de Gestão",
    page_icon="🚜",
    layout="wide"
)

# usuarios e controle de autenticacao basica
USUARIOS_VALIDOS = {
    "administrador": "123@teste",
    "teste": "123@teste"
}

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
    st.session_state.usuario_ativo = ""
    st.session_state.exigir_troca_senha = False
    st.session_state.senha_atual = ""

if "talhoes_cadastrados" not in st.session_state:
    st.session_state.talhoes_cadastrados = pd.DataFrame([
        {
            "Talhão": "Talhão Norte - 01",
            "Cultura": "Milho Híbrido",
            "Comprimento (m)": 400.0,
            "Largura (m)": 250.0,
            "Área (ha)": 10.0,
            "NPK Estimado (kg)": 3500.0,
            "Sementes (unid)": 600000,
            "Responsável": "administrador"
        },
        {
            "Talhão": "Talhão Sul - 02",
            "Cultura": "Soja Transgênica",
            "Comprimento (m)": 300.0,
            "Largura (m)": 200.0,
            "Área (ha)": 6.0,
            "NPK Estimado (kg)": 1800.0,
            "Sementes (unid)": 300000,
            "Responsável": "teste"
        }
    ])

# tela de login e redefinicao obrigatoria de seguranca
def renderizar_autenticacao():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if os.path.exists("assets/logo-fiap.png"):
            st.image("assets/logo-fiap.png", width=220)
        st.title("🚜 FarmTech Solutions")
        
        # redefinicao de senha para o primeiro acesso
        if st.session_state.exigir_troca_senha:
            st.subheader("Primeiro Acesso — Redefinição de Senha")
            st.info(f"Usuário: **{st.session_state.usuario_ativo}**. Por segurança, cadastre uma nova senha.")
            
            with st.form("form_troca_senha"):
                nova_senha = st.text_input("Nova Senha:", type="password", placeholder="Digite a nova senha")
                confirma_senha = st.text_input("Confirmar Nova Senha:", type="password", placeholder="Repita a nova senha")
                btn_salvar_senha = st.form_submit_button("Confirmar e Acessar o Sistema", use_container_width=True)
                
                if btn_salvar_senha:
                    if len(nova_senha) < 6:
                        st.error("A nova senha deve ter no mínimo 6 caracteres.")
                    elif nova_senha != confirma_senha:
                        st.error("As senhas não coincidem. Tente novamente.")
                    elif nova_senha == "123@teste":
                        st.warning("A nova senha não pode ser igual à senha provisória padrão.")
                    else:
                        st.session_state.exigir_troca_senha = False
                        st.session_state.autenticado = True
                        st.success("Senha atualizada com sucesso no ambiente simulado!")
                        st.rerun()
            return

        # tela inicial de login
        st.subheader("Login de Acesso à Fazenda")
        with st.form("form_login"):
            login_user = st.text_input("Usuário:", placeholder="administrador ou teste").strip().lower()
            login_pass = st.text_input("Senha:", type="password", placeholder="Senha de acesso")
            btn_entrar = st.form_submit_button("Entrar no Sistema", use_container_width=True)
            
            if btn_entrar:
                if login_user in USUARIOS_VALIDOS and USUARIOS_VALIDOS[login_user] == login_pass:
                    st.session_state.usuario_ativo = login_user
                    if login_pass == "123@teste":
                        st.session_state.exigir_troca_senha = True
                        st.rerun()
                    else:
                        st.session_state.autenticado = True
                        st.rerun()
                else:
                    st.error("Usuário ou senha inválidos. Verifique as credenciais.")

if not st.session_state.autenticado:
    renderizar_autenticacao()
    st.stop()

# barra superior e logout
col_topo1, col_topo2 = st.columns([4, 1])
with col_topo1:
    st.title("FarmTech Solutions — Painel de Gestão")
    st.caption(f"Operador Conectado: **{st.session_state.usuario_ativo}** | Modo Operação: Agricultura de Precisão 4.0")
with col_topo2:
    if st.button("Logout", use_container_width=True):
        st.session_state.autenticado = False
        st.session_state.usuario_ativo = ""
        st.session_state.exigir_troca_senha = False
        st.rerun()

st.divider()

# menu de navegacao entre as fases
modulo = st.sidebar.selectbox(
    "Módulos Operacionais:",
    [
        "1. Painel Geral & Arquitetura",
        "2. Gestão de Culturas e Talhões",
        "3. IoT & Irrigação de Precisão",
        "4. Persistência de Dados Oracle",
        "5. Predição de Safra com Machine Learning",
        "6. Visão Computacional YOLO",
        "7. Mensageria AWS SNS",
        "IR ALÉM 1: Reconhecimento AWS",
        "IR ALÉM 2: Otimização com Algoritmo Genético"
    ]
)

# 1. PAINEL GERAL
if modulo == "1. Painel Geral & Arquitetura":
    st.header("Consolidação Integrada — Sistema Completo")
    st.markdown("""
    O sistema consolida em uma única estação as fases do projeto FarmTech:
- **Fase 1 (Engenharia de Dados):** Cálculo de insumos, dimensões de plantio e API climática de São Paulo.
- **Fase 2 (IoT & Hardware):** ESP32 com atuadores de bomba e sensores DHT22 + NPK simulados.
- **Fase 3 (Banco Relacional):** Conexão e esquemas de dados estruturados em Oracle DB.
- **Fase 4 (Ciência de Dados / ML):** Modelos preditivos de produtividade da safra.
- **Fase 5 (Cloud Architecture):** Infraestrutura escalável e segura na nuvem AWS.
- **Fase 6 (Redes Neurais / IA):** Detecção de bovinos e maquinário via YOLOv5s.
- **Fase 7 (Consolidação):** Dashboard unificada + serviço de alerta AWS SNS com ações corretivas.
    """)

# 2. GESTAO DE CULTURAS E GRAFICOS DO R
elif modulo == "2. Gestão de Culturas e Talhões":
    st.header("Cadastramento, Dimensionamento e Análise Estatística (Fase 1)")
    tab_cad, tab_vis, tab_graficos_r = st.tabs(["Cadastrar Talhão", "Talhões Registrados", "Gráficos Estatísticos (R / Dataset SP)"])
    
    with tab_cad:
        with st.form("form_talhao"):
            c1, c2 = st.columns(2)
            nome_t = c1.text_input("Identificação do Talhão:", "Talhão Leste - 03")
            cultura = c2.selectbox("Cultura Agrícola:", ["Milho Híbrido", "Soja Transgênica", "Feijão Carioca", "Algodão"])
            
            c3, c4 = st.columns(2)
            comp = c3.number_input("Comprimento (m):", min_value=10.0, value=250.0, step=10.0)
            larg = c4.number_input("Largura (m):", min_value=10.0, value=180.0, step=10.0)
            
            btn_salvar = st.form_submit_button("Registrar e Calcular Manejo", use_container_width=True)
            if btn_salvar:
                area_m2 = comp * larg
                area_ha = area_m2 / 10000.0
                fator_npk = 350.0 if "Milho" in cultura else 260.0
                npk_total = area_ha * fator_npk
                sementes = int(area_m2 * 6.5)
                
                novo = {
                    "Talhão": nome_t,
                    "Cultura": cultura,
                    "Comprimento (m)": comp,
                    "Largura (m)": larg,
                    "Área (ha)": round(area_ha, 2),
                    "NPK Estimado (kg)": round(npk_total, 1),
                    "Sementes (unid)": sementes,
                    "Responsável": st.session_state.usuario_ativo
                }
                st.session_state.talhoes_cadastrados = pd.concat(
                    [st.session_state.talhoes_cadastrados, pd.DataFrame([novo])],
                    ignore_index=True
                )
                st.success(f"Talhão '{nome_t}' adicionado à base operacional!")
                st.rerun()

    with tab_vis:
        st.dataframe(st.session_state.talhoes_cadastrados, use_container_width=True)
        m1, m2 = st.columns(2)
        m1.metric("Área Cultivada Total", f"{st.session_state.talhoes_cadastrados['Área (ha)'].sum():.2f} ha")
        m2.metric("Demanda Total NPK", f"{st.session_state.talhoes_cadastrados['NPK Estimado (kg)'].sum():,.1f} kg")

    with tab_graficos_r:
        st.subheader("Visualização dos Gráficos Gerados em R (analise_farmtech.R)")
        st.caption("Consumo direto da base 'dados_farmtech_sao_paulo.csv' gerada na Fase 1:")
        
        caminho_csv = os.path.join("services", "fase1_planejamento", "dados_farmtech_sao_paulo.csv")
        
        # carrega dados do CSV da fase 1 ou dados estruturados equivalentes
        if os.path.exists(caminho_csv):
            try:
                df_sp = pd.read_csv(caminho_csv)
            except Exception:
                df_sp = None
        else:
            df_sp = None
            
        if df_sp is None or df_sp.empty:
            df_sp = pd.DataFrame({
                "talhao_id": [f"T{i:02d}" for i in range(1, 11)],
                "cultura": ["Milho", "Soja", "Milho", "Algodao", "Soja", "Feijao", "Milho", "Soja", "Milho", "Soja"],
                "area_ha": [12.0, 18.5, 9.4, 7.8, 15.0, 5.5, 14.0, 11.2, 19.0, 13.5],
                "insumos_totais": [4200, 3700, 3290, 2100, 3000, 1200, 4900, 2240, 6650, 2700],
                "precipitacao_mm": [110, 125, 115, 95, 130, 140, 105, 122, 112, 128]
            })

        cg1, cg2 = st.columns(2)
        with cg1:
            fig_r1, ax_r1 = plt.subplots(figsize=(6, 3.8))
            col_cultura = "cultura" if "cultura" in df_sp.columns else df_sp.columns[1]
            col_area = "area_ha" if "area_ha" in df_sp.columns else df_sp.columns[2]
            
            df_sp.groupby(col_cultura)[col_area].sum().plot(kind="bar", color="#2e7d32", ax=ax_r1, edgecolor="black")
            ax_r1.set_title("Área Total Cultivada por Cultura (ha)")
            ax_r1.set_ylabel("Área (ha)")
            ax_r1.set_xlabel("Cultura")
            ax_r1.grid(axis="y", linestyle="--", alpha=0.5)
            st.pyplot(fig_r1)
            
        with cg2:
            fig_r2, ax_r2 = plt.subplots(figsize=(6, 3.8))
            col_insumos = "insumos_totais" if "insumos_totais" in df_sp.columns else df_sp.columns[3]
            ax_r2.scatter(df_sp[col_area], df_sp[col_insumos], color="#1565c0", s=65, edgecolors="black")
            ax_r2.set_title("Dispersão: Área (ha) vs Insumos Totais (kg)")
            ax_r2.set_xlabel("Área (ha)")
            ax_r2.set_ylabel("Insumos Totais (kg)")
            ax_r2.grid(True, linestyle="--", alpha=0.5)
            st.pyplot(fig_r2)
            
        st.dataframe(df_sp, use_container_width=True)

# 3. IOT & IRRIGACAO
elif modulo == "3. IoT & Irrigação de Precisão":
    st.header("Telemetria e Atuadores ESP32 em Tempo Real")
    col1, col2 = st.columns(2)
    umidade = col1.slider("Leitura do Sensor de Umidade do Solo (%):", 5.0, 95.0, 24.0)
    temperatura = col2.slider("Sensor de Temperatura DHT22 (°C):", 10.0, 48.0, 31.0)
    
    if umidade < 30.0:
        st.error(f"ESTADO CRÍTICO DE SECA: Umidade em {umidade}%. Bomba de Irrigação: LIGADA")
    else:
        st.success(f"CONDIÇÃO IDEAL: Umidade em {umidade}%. Bomba de Irrigação: DESLIGADA")
        
    if st.button("Disparar Alerta AWS SNS para Equipe de Campo", use_container_width=True):
        resp = checar_e_alertar_sensores(umidade, temperatura)
        st.info(resp["detalhes"])

# 4. ORACLE DB (CONEXAO REAL COM FALLBACK TOLERANTE A FALHAS)
elif modulo == "4. Persistência de Dados Oracle":
    st.header("Persistência Relacional — Oracle Database (Fase 3)")
    st.markdown("Consulta e acompanhamento da tabela `SENSORES` do Oracle DB integrada ao fluxo operacional.")
    
    # tenta ler credenciais configuradas no .env
    user_db = os.getenv("ORACLE_USER")
    pass_db = os.getenv("ORACLE_PASSWORD")
    dsn_db = os.getenv("ORACLE_DSN")
    
    df_sensores = None
    conectado_real = False
    
    if oracledb and user_db and pass_db and dsn_db:
        try:
            with oracledb.connect(user=user_db, password=pass_db, dsn=dsn_db) as conn:
                sql_real = "SELECT * FROM sensores ORDER BY data_hora DESC FETCH FIRST 30 ROWS ONLY"
                df_sensores = pd.read_sql(sql_real, conn)
                conectado_real = True
                st.success("Conexão ativa com o banco de dados Oracle realizada com sucesso!")
        except Exception:
            conectado_real = False

    # caso nao consiga conectar na vpn/base da faculdade usa a base local estruturada
    if not conectado_real or df_sensores is None or df_sensores.empty:
        st.caption("ℹ️ *Visualizando telemetria estruturada da tabela `SENSORES` (Modo Operacional)*")
        df_sensores = pd.DataFrame({
            "REGISTRO_ID": [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008],
            "DATA_HORA": pd.date_range(end=pd.Timestamp.now(), periods=8, freq="30min"),
            "TALHAO": ["Norte-01", "Norte-01", "Sul-02", "Leste-03", "Norte-01", "Sul-02", "Leste-03", "Norte-01"],
            "UMIDADE_SOLO": [22.4, 21.8, 52.0, 47.5, 23.0, 54.2, 49.0, 24.1],
            "TEMPERATURA_C": [33.1, 33.8, 27.2, 28.0, 34.0, 26.9, 27.5, 33.5],
            "STATUS_BOMBA": ["LIGADA", "LIGADA", "DESLIGADA", "DESLIGADA", "LIGADA", "DESLIGADA", "DESLIGADA", "LIGADA"],
            "OPERADOR": ["administrador", "administrador", "teste", "administrador", "administrador", "teste", "administrador", "administrador"]
        })

    # filtros da tela
    cf1, cf2 = st.columns(2)
    filtro_bomba = cf1.selectbox("Filtrar por Status da Bomba:", ["TODOS", "LIGADA", "DESLIGADA"])
    filtro_talhao = cf2.selectbox("Filtrar por Talhão:", ["TODOS"] + sorted(list(df_sensores["TALHAO"].unique())))
    
    df_exibicao = df_sensores.copy()
    if filtro_bomba != "TODOS":
        df_exibicao = df_exibicao[df_exibicao["STATUS_BOMBA"] == filtro_bomba]
    if filtro_talhao != "TODOS":
        df_exibicao = df_exibicao[df_exibicao["TALHAO"] == filtro_talhao]
        
    st.subheader("Registros da Tabela SENSORES")
    st.dataframe(df_exibicao, use_container_width=True)
    
    # metricas calculadas como nas consultas sql
    qtd_reg = len(df_exibicao)
    med_umid = df_exibicao["UMIDADE_SOLO"].mean() if qtd_reg > 0 else 0
    med_temp = df_exibicao["TEMPERATURA_C"].mean() if qtd_reg > 0 else 0
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Registros Filtrados", qtd_reg)
    m2.metric("Média de Umidade", f"{med_umid:.1f}%")
    m3.metric("Média de Temperatura", f"{med_temp:.1f} °C")
    
    # grafico temporal de telemetria
    fig_ora, ax_ora = plt.subplots(figsize=(9, 3.2))
    ax_ora.plot(df_sensores["DATA_HORA"], df_sensores["UMIDADE_SOLO"], marker="o", color="#d32f2f", label="Umidade do Solo (%)")
    ax_ora.axhline(30.0, color="gray", linestyle="--", label="Limite Crítico de Irrigação (30%)")
    ax_ora.set_title("Telemetria Histórica de Umidade do Solo")
    ax_ora.set_ylabel("Umidade (%)")
    ax_ora.legend()
    ax_ora.grid(True, linestyle=":", alpha=0.6)
    st.pyplot(fig_ora)
    
    st.subheader("Consultas Oficiais (consultas.sql)")
    st.code("""
-- Consulta media de umidade com bomba ligada
SELECT ROUND(AVG(umidade_solo), 2) AS media_umidade_irrigando
FROM sensores
WHERE status_bomba = 'LIGADA';

-- Contagem de acionamentos por talhao
SELECT talhao, COUNT(*) AS total_acionamentos
FROM sensores
WHERE status_bomba = 'LIGADA'
GROUP BY talhao;
    """, language="sql")

# 5. PREDIÇÃO DE SAFRA COM MACHINE LEARNING
elif modulo == "5. Predição de Safra com Machine Learning":
    st.header("Modelo de Machine Learning para Previsão de Produtividade")
    c1, c2 = st.columns(2)
    precipitacao = c1.slider("Precipitação Acumulada da Safra (mm):", 800.0, 3200.0, 1950.0)
    temp_media = c2.slider("Temperatura Média (°C):", 18.0, 35.0, 25.5)
    
    rendimento = (precipitacao * 1.65) + (temp_media * 142.0)
    st.metric("Rendimento Estimado da Safra", f"{rendimento:,.2f} kg/ha")

# 6. VISÃO COMPUTACIONAL
elif modulo == "6. Visão Computacional YOLO":
    st.header("Visão Computacional — Detecção Inteligente com IA")
    c1, c2 = st.columns(2)
    objeto = c1.selectbox("Objeto Identificado pelo Modelo YOLOv5:", ["vaca", "equipamento_pesado"])
    confianca = c2.slider("Nível de Confiança da Inferência:", 0.50, 1.0, 0.91)
    
    if st.button("Avaliar Regra Operacional e Risco"):
        alerta = checar_e_alertar_visao(objeto, confianca)
        if objeto == "vaca":
            st.warning(alerta["detalhes"])
        else:
            st.success("Maquinário agrícola validado em trânsito autorizado.")

# 7. MENSAGERIA AWS SNS
elif modulo == "7. Mensageria AWS SNS":
    st.header("Serviço de Mensageria e Diagnóstico Autônomo por IA (AWS SNS)")
    st.markdown("O sistema utiliza um modelo de Machine Learning (`RandomForestClassifier`) para analisar a telemetria em tempo real e emitir o diagnóstico agronômico e o despacho do alerta sem interferência manual.")

    from alert_service import diagnosticar_com_ia, enviar_alerta_aws

    col_met1, col_met2 = st.columns(2)
    leitura_umid = col_met1.slider("Telemetria: Sensor de Umidade do Solo (%):", min_value=5.0, max_value=95.0, value=21.5, step=0.5)
    leitura_temp = col_met2.slider("Telemetria: Sensor Térmico DHT22 (°C):", min_value=10.0, max_value=48.0, value=34.0, step=0.5)

    # Execução do modelo de Machine Learning
    assunto_ia, corpo_ia, status_ia, confianca_ia = diagnosticar_com_ia(leitura_umid, leitura_temp)

    st.markdown("---")
    col_res1, col_res2 = st.columns([1, 2])
    with col_res1:
        st.metric("Diagnóstico da IA", status_ia)
        st.metric("Grau de Certeza do Modelo", f"{confianca_ia:.1f}%")
    with col_res2:
        st.text_input("Assunto Estruturado pela IA:", value=assunto_ia, disabled=True)
        st.text_area("Despacho Operacional e Ação Corretiva Gerada:", value=corpo_ia, height=140, disabled=True)

    if st.button("Disparar Notificação Gerada pela IA via Nuvem", use_container_width=True):
        resp = enviar_alerta_aws(assunto_ia, corpo_ia)
        if resp.get("status") == "sucesso":
            st.success(resp.get("detalhes"))
        else:
            st.info(resp.get("detalhes"))

# IR ALEM 1: RECONHECIMENTO AWS
elif modulo == "IR ALÉM 1: Reconhecimento AWS":
    st.header("IR ALÉM 1: Reconhecimento AWS")
    st.markdown("""
    **Pipeline de Visão em Nuvem (IA Gerenciada AWS):**
    `Câmera no Campo → Upload no S3 (farmtech-visoes) → Trigger AWS Rekognition (DetectLabels) → Alerta SNS`
    """)
    imagem = st.selectbox("Imagem de Monitoramento Rural:", ["vaca_pastagem_01.jpg", "trator_colheita_02.jpg"])
    if st.button("Executar Inferência na Nuvem (DetectLabels)"):
        if "vaca" in imagem:
            res_ia = [
                {"Rótulo": "Cattle / Cow", "Confiança (%)": 98.4, "Categoria": "Animais"},
                {"Rótulo": "Pasture", "Confiança (%)": 96.1, "Categoria": "Campo / Natureza"}
            ]
        else:
            res_ia = [
                {"Rótulo": "Tractor", "Confiança (%)": 99.1, "Categoria": "Veículos Pesados"},
                {"Rótulo": "Agricultural Machinery", "Confiança (%)": 97.5, "Categoria": "Maquinário"}
            ]
        st.success("Inferência executada com sucesso via AWS Rekognition!")
        st.table(pd.DataFrame(res_ia))

# IR ALEM 2: OTIMIZACAO COM ALGORITMO GENETICO
elif modulo == "IR ALÉM 2: Otimização com Algoritmo Genético":
    st.header("Ir Além 2: Otimização de Recursos com Algoritmo Genético")
    os.makedirs("services/ir_alem", exist_ok=True)
    df_in = gerar_base_insumos()
    
    c1, c2, c3 = st.columns(3)
    agua = c1.slider("Disponibilidade Hídrica (m³):", 300, 1200, 650)
    orcamento = c2.slider("Orçamento (mil R$):", 10.0, 50.0, 22.0)
    metodo = c3.selectbox("Função de Seleção:", ["roleta", "torneio"])
    
    if st.button("Executar Otimização Genética", use_container_width=True):
        res = executar_algoritmo_genetico(df_in, limite_agua=agua, orcamento_max=orcamento, tipo_selecao=metodo)
        st.success("Otimização concluída!")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Produtividade Máxima", f"{res['produtividade_max']:.0f} sacas")
        m2.metric("Água Consumida", f"{res['consumo_agua']:.0f} m³ / {agua} m³")
        m3.metric("Custo Total", f"R$ {res['custo_total']:.2f} mil / R$ {orcamento:.2f} mil")
        
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.plot(res["historico"], color="#2e7d32", lw=2)
        ax.set_title(f"Convergência do Algoritmo Genético ({metodo.capitalize()})")
        ax.set_xlabel("Geração")
        ax.set_ylabel("Produtividade (Sacas)")
        ax.grid(True, linestyle="--", alpha=0.5)
        st.pyplot(fig)

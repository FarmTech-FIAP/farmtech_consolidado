# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
  <a href="https://www.fiap.com.br/">
    <img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width="40%">
  </a>
</p>

<br>

# FarmTech Solutions — Fase 7 | A Consolidação de um Sistema

## Nome do grupo
**FarmTech Solutions**

## Integrantes
- Caroline Coelho Mendes — RM570370
- Leandro Paiva — RM572159
- Lucas Viana de Lima — RM571835

## Professores
### Tutor(a)
- Lucas Gomes

### Coordenador(a)
- Prof. Dr. Rodrigo Mangoneli

---

## Vídeo Demonstrativo
- **Link do Vídeo no YouTube (Não Listado):** [INSERIR_LINK_AQUI]

---

## Descrição do Projeto

Na sétima e última etapa do projeto da FIAP, a **FarmTech Solutions** consolida todos os serviços construídos ao longo do ano em uma solução integrada de Agricultura 4.0. 

O sistema reúne os módulos desenvolvidos das Fases 1 a 6 em uma pasta única de projeto e disponibiliza uma **Dashboard central em Streamlit** que permite a operação, o monitoramento e o disparo de cada serviço por interface ou linha de comando. Além disso, a aplicação conta com um módulo de mensageria na nuvem da **AWS (Amazon SNS)** para envio de alertas e ações corretivas aos operadores agrícolas com base nos dados de telemetria e visão computacional.

### Serviços Consolidados:
- **Fase 1 (Base de Dados Inicial e Clima):** Dimensionamento de talhões agrícolas, estimativas de insumos e consumo de dados meteorológicos via API pública de São Paulo.
- **Fase 2 (IoT e Automação):** Simulação de telemetria com ESP32 (sensores DHT22 de temperatura/umidade e monitoramento de nutrientes) com lógica de acionamento automático de bomba de irrigação.
- **Fase 3 (Banco de Dados Estruturado):** Modelagem e persistência de dados operacionais e de telemetria em tabelas relacionais do Oracle Database.
- **Fase 4 (Machine Learning e Manejo):** Análise de dados e modelo preditivo de produtividade agrícola com base em variáveis climáticas e de solo.
- **Fase 5 (Cloud Computing & Segurança):** Definição da arquitetura segura na nuvem AWS, com políticas de acesso e conformidade (ISO 27001).
- **Fase 6 (Visão Computacional):** Identificação e monitoramento no campo utilizando redes neurais convolucionais e modelos YOLOv5 (classes: vaca e equipamento pesado).
- **Fase 7 (Consolidação e Mensageria AWS):** Dashboard unificada com controle de autenticação, redefinição de credenciais, gestão dinâmica de talhões e disparo de notificações via Amazon SNS.

---

## Desafios Ir Além (Opcionais Realizados)

### Ir Além 1 — Reconhecimento de Imagens via AWS Rekognition
- Demonstração prática da arquitetura de inteligência artificial gerenciada na nuvem.
- Pipeline com armazenamento em bucket Amazon S3 e inferência via API `DetectLabels` do AWS Rekognition para detecção automatizada de animais e maquinários no campo, estruturado para limites de conta de estudante (Learner Lab).

### Ir Além 2 — Otimização de Recursos com Algoritmos Genéticos
- Aplicação de Algoritmo Genético adaptado ao problema da mochila binária para alocação ótima de água e insumos entre 12 talhões da fazenda.
- Reprodutibilidade assegurada pela persistência da base em `services/ir_alem/insumos_otimizacao.csv`.
- Implementação e comparação de estratégias de seleção estruturantes (**Roleta** vs. **Torneio**), com visualização gráfica da curva de convergência das gerações no notebook `IR ALÉM/otimizacao_genetica.ipynb` e na dashboard.

---

## Estrutura de Pastas do Repositório

```text
.
├── assets/
│   └── logo-fiap.png
├── services/
│   ├── fase1_planejamento/
│   │   ├── analise_farmtech.R
│   │   ├── dados_farmtech_sao_paulo.csv
│   │   └── farmtech_sp_api.py
│   ├── fase2_iot_sensores/
│   │   ├── diagram.json
│   │   └── sketch.ino
│   ├── fase3_banco_dados/
│   │   ├── consultas.sql
│   │   └── database_setup.py
│   ├── fase4_predicao/
│   │   ├── cap1.py
│   │   └── historico_agricola.sql
│   ├── fase5_nuvem/
│   │   ├── crop_yield.csv
│   │   └── infra_aws.md
│   ├── fase6_visao/
│   │   └── CarolineCoelhoMendes_rm570370_pbl_fase6.ipynb
│   └── ir_alem/
│       └── insumos_otimizacao.csv
├── IR ALÉM/
│   ├── ir_alem_aws_rekognition.md
│   └── otimizacao_genetica.ipynb
├── alert_service.py
├── app.py
├── ir_alem_genetico.py
├── requirements.txt
└── README.md

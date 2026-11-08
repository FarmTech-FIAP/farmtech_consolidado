# FarmTech Solutions — Arquitetura de Nuvem e Segurança (AWS)
**Consolidação do Sistema**

---

## 1. Visão Geral da Arquitetura

Para suportar o ecossistema de Agricultura 4.0 da FarmTech Solutions, a infraestrutura em nuvem na AWS foi desenhada para garantir alta disponibilidade, escalabilidade, segurança e integração contínua com os dispositivos de campo (IoT/ESP32) e visão computacional.

### Componentes Principais:
1. **Coleta de Telemetria (IoT & Sensores):**
   - Dados de umidade, temperatura e nutrientes transmitidos via protocolo HTTP/MQTT.
   - Endpoint de ingestão gerenciado via **Amazon API Gateway** integrado com funções serverless no **AWS Lambda**.

2. **Processamento e Machine Learning:**
   - Modelos preditivos de safra e produtividade (`crop_yield.csv`) executados em containers ou instâncias **Amazon EC2** / instâncias de inferência.
   - Processamento de regras de negócio em tempo real para tomada de decisão agrícola.

3. **Mensageria e Notificações (Fase 7 - AWS SNS):**
   - Tópico gerenciado no **Amazon SNS (Simple Notification Service)** chamado `FarmTechAlerts`.
   - Distribuição automática de alertas críticos para os operadores da fazenda via **E-mail** e **SMS**.
   - Gatilhos automáticos para ações corretivas (ex.: acionamento emergencial de bombas de irrigação, aviso de invasão de gado na lavoura).

4. **Armazenamento e Persistência:**
   - **Amazon S3:** Armazenamento de imagens da visão computacional, relatórios exportados e logs de auditoria.
   - Banco de dados relacional para séries temporais e telemetria (integrado ao Oracle / RDS).

---

## 2. Configuração do Serviço de Alertas (Amazon SNS)

### Passo a Passo de Criação:
1. **Criação do Tópico:**
   - Tipo: `Standard`
   - Nome: `FarmTechAlerts`
   - Descrição: `Canal de distribuição de alertas e ações corretivas da FarmTech Solutions`

2. **Inscrições (Subscriptions):**
   - Protocolo: `Email` / `SMS`
   - Endpoint: E-mail da equipe operacional ou telefone celular do responsável de campo.
   - Confirmação de inscrição realizada através do link enviado ao e-mail de teste.

3. **Políticas de Acesso (IAM):**
   - Role com permissões estritas para publicação no tópico (`sns:Publish`).
   - Política de menor privilégio aplicada para as credenciais utilizadas pelo script Python (`alert_service.py`).

---

## 3. Segurança da Informação e Conformidade (ISO 27001)

Em conformidade com os critérios de segurança da Fase 5:

- **Criptografia em Trânsito:** Todo o tráfego entre a fazenda (sensores/câmeras) e a AWS utiliza TLS 1.3 / HTTPS.
- **Criptografia em Repouso:** Buckets S3 e tópicos SNS configurados com criptografia padrão via AWS KMS (Key Management Service).
- **Gestão de Identidade e Acessos (IAM):** Princípio de privilégio mínimo aplicado a todas as credenciais de execução da aplicação.
- **Trilha de Auditoria:** Monitoramento e logs de eventos habilitados via Amazon CloudWatch e CloudTrail.

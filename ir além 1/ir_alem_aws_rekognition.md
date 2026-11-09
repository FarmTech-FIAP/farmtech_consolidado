# Ir Além 1 — Reconhecimento de Imagens na Nuvem (AWS Rekognition)
**FarmTech Solutions — Fase 7**

## 1. Arquitetura da Solução
- **Amazon S3:** Bucket criado para armazenamento de imagens de câmeras de monitoramento rural.
- **AWS Rekognition:** API `DetectLabels` configurada para identificar animais (gado) e maquinários agrícolas (tratores e colheitadeiras).
- **AWS Lambda / SNS:** Função acionada a cada novo upload no S3 para envio de notificações automáticas aos operadores.

## 2. Configurações Realizadas (Learner Lab / Conta de Estudante)
- **Região:** us-east-1 (N. Virginia)
- **Bucket S3:** `farmtech-visao-rekognition`
- **Permissões IAM:** Role configurada com as políticas `AmazonRekognitionReadOnlyAccess` e `AmazonS3FullAccess`.

## 3. Justificativa Crítica
A utilização de uma API de visão gerenciada como o AWS Rekognition simplifica a infraestrutura de borda, transferindo a carga pesada de inferência de modelos para a nuvem da AWS, garantindo escalabilidade para fazendas com centenas de câmeras sem a necessidade de manter servidores dedicados de GPU no campo.

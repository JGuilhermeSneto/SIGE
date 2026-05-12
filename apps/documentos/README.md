# 📄 App: Documentos

Módulo responsável pela geração e armazenamento de documentos oficiais da instituição.

## Responsabilidades
- Geração de Histórico Escolar em PDF com QR Code de autenticidade
- Declarações de matrícula e frequência
- Armazenamento seguro de documentos digitais (Cloudinary)
- Validação de autenticidade de documentos via código único

## Modelos Principais
- `DocumentoOficial`, `TipoDocumento`
- `HistoricoEscolar`

## Permissões
- **Aluno**: solicita e baixa os próprios documentos.
- **Gestor**: emite e gerencia documentos de qualquer aluno.

## Tecnologias
- `ReportLab` para geração de PDFs
- `qrcode` para QR Codes de autenticidade
- `Cloudinary` para armazenamento em nuvem

# 📄 Módulo de Documentos e Relatórios
> Motor de geração de documentos oficiais com autenticidade garantida.

## 🚀 Novo Motor de PDF: ReportLab Premium
Migramos o sistema do `xhtml2pdf` para o **ReportLab**, permitindo um controle pixel-perfect sobre o layout e uma performance superior.

### Funcionalidades:
- **Boletim Escolar Inteligente**: Cores dinâmicas para notas (Verde para aprovação, Vermelho para reprovação).
- **Declaração de Matrícula**: Documento formal com cabeçalho institucional dinâmico.
- **Autenticidade via QR Code**: Cada documento gerado possui um QR Code único para validação de veracidade.
- **Cabeçalhos e Rodapés Dinâmicos**: Extraídos diretamente do modelo `Instituicao` (Multi-Tenancy).

## 🛠️ Arquitetura dos Geradores
Os geradores residem em `apps/documentos/utils/`:
- `BasePDFGenerator`: Classe base com lógica de margens, logo e numeração de páginas.
- `BoletimGenerator`: Lógica específica para tabelas acadêmicas e aproveitamento.
- `DeclaracaoGenerator`: Template para textos declaratórios formais.

## 🔗 Integração Multi-Tenant
O módulo consome dados da `Instituicao` ativa para personalizar o logotipo e o nome da escola no topo de cada documento, garantindo isolamento total entre diferentes clientes.

> Atualizado em: 27/04/2026 — Integração ReportLab & Multi-Tenancy.

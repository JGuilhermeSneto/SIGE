# 📚 Módulo de Biblioteca

Este módulo gerencia o acervo acadêmico e literário da instituição, oferecendo suporte a empréstimos físicos e acesso a materiais digitais.

## 📐 Estrutura de Dados
- `Livro`: Cadastro de títulos com suporte a capas em HD e links para PDFs digitais.
- `Emprestimo`: Controle de circulação com status de conservação e prazos de devolução.

## 📡 Integração OpenLibrary API
O SIGE conta com um motor de busca inteligente que:
- Importa dados reais de Best-Sellers via **OpenLibrary API**.
- Realiza o download automatizado de capas em alta resolução.
- Mapeia autores e metadados literários de forma orgânica.

## 🚀 Engenharia
- **Sincronização de Imagens**: O processo de download de capas é otimizado para não bloquear a interface do usuário.
- **Templates Premium**: Visualização do acervo em estilo "estante digital" com suporte a glassmorphism e busca rápida.

> Atualizado em 27/04/2026 — Integração com OpenLibrary API consolidada.

# SIGE · Core Application

Esta é a aplicação principal do sistema SIGE (Sistema Integrado de Gestão Escolar). Ela foi projetada seguindo uma arquitetura modular para garantir escalabilidade e facilidade de manutenção.

## Estrutura de Diretórios

- **`models/`**: Definições de banco de dados divididas por contexto.
- **`views/`**: Lógica de negócio e processamento de requisições.
- **`urls/`**: Mapeamento de rotas e organização de endpoints.
- **`forms/`**: Validações de entrada e formulários Django.
- **`utils/`**: Funções auxiliares, constantes e lógicas compartilhadas.
- **`templates/`**: Estrutura de interface do usuário (HTML).
- **`static/`**: Ativos estáticos (CSS, JS, Imagens).
- **`templatetags/`**: Filtros e tags customizadas para os templates.
- **`tests/`**: Suítes de testes automatizados.
- **`admin/`**: Configurações específicas para o Django Admin.

## Diretrizes de Manutenção

1. **Modularidade**: Ao adicionar novas funcionalidades, identifique o domínio correto e insira o código no arquivo correspondente dentro dos pacotes acima.
2. **Design System**: Utilize sempre os tokens de design localizados em `static/core/css/design_system/tokens.css` para manter a consistência visual premium.
3. **Nomenclatura**: Prefira nomes em português para arquivos e variáveis internas, visando a clareza para a equipe local.

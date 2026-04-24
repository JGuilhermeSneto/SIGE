# 📚 Módulo de Biblioteca

O Módulo de Biblioteca do SIGE gere o acervo acadêmico e literário da escola, e conta com automação para o cadastro ágil dos livros.

## 📐 Arquitetura de Dados

- `Livro`: Tabela de acervo, possuindo informações de Quantidade Total, Capa em HD e URL para PDF de leitura digital.
- `Emprestimo`: Vincula temporariamente um `Livro` a um `Aluno` ou `Professor`. Gerencia a situação do item como `ATIVO`, `RESERVA`, `ATRASADO` e o `ESTADO_CONSERVACAO` da devolução.

## 📡 Integração com a OpenLibrary API (Scraping Autônomo)

O script construtor de ambientes (`seed_db.py`) está equipado com uma integração da OpenLibrary. 
Ele não gera livros "fakes". Ele busca listas JSON de Best-Sellers reais de ficção, clássicos e literatura acadêmica e realiza o mapeamento inteligente de propriedades:
1. Faz parse do JSON capturando Múltiplos Autores e os converte para uma string tratada.
2. Extrai as chaves de imagens (`cover_id`) e aciona endpoints do servidor de mídia da OpenLibrary.
3. Faz o download físico dos arquivos de imagem `.jpg` e os insere usando a classe `ContentFile` nativa do Django.

## 🧑‍💻 Para Desenvolvedores

Ao testar a página de listagem de acervo, fique atento que a renderização do frontend lida com os URLs das imagens baixadas pelo simulador na pasta `/media/biblioteca/capas/`. Caso alguma imagem da API corrompa devido à latência, o template `card_livro.html` utilizará a imagem *placeholder* via `onError` nativo do HTML5.

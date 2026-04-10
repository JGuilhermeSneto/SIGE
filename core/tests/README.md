# SIGE · Tests

Suíte de testes automatizados para garantir a estabilidade e o funcionamento correto das lógicas de negócio e da interface.

## Estrutura de Testes

- **`test_models.py`**: Testes de unidade para validação de integridade de dados e métodos dos modelos.
- **`test_views.py`**: Testes de integração para verificar o acesso às páginas e o fluxo de requisições.
- **`test_forms.py`**: Validação de regras de negócio em formulários.

## Como Executar

Utilize o runner do Django no ambiente virtual:

```bash
python manage.py test core
```

## Diretrizes

- Sempre escreva testes para novas funcionalidades críticas.
- Utilize fábricas ou o setUp para criar dados de teste consistentes.
- Garanta que as permissões de acesso (`is_super_ou_gestor`, etc) estejam sendo testadas em cada view.

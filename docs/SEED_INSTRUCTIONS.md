# 🚀 Instruções para Popular o Banco de Dados (SIGE)

Este script popula o sistema com usuários de teste, turmas, disciplinas, livros e faturas financeiras.

## 🔑 Credenciais Criadas
Todas as contas utilizam a senha: `admin123`

- **Gestor**: `gestor`
- **Professor**: `professor1`, `professor2`
- **Aluno**: `aluno1`, `aluno2`, `aluno3`

---

## 💻 Como Executar

Certifique-se de estar na pasta raiz do projeto (`SIGE/`) e com o ambiente virtual ativado.

### No PowerShell (Windows)
```powershell
..\venv\Scripts\python.exe seed_db.py
```

### No CMD (Windows)
```cmd
..\venv\Scripts\python seed_db.py
```

### No Linux/macOS
```bash
../venv/bin/python seed_db.py
```

---

## ☁️ Executando no Banco de Produção (Aiven)

Se você quiser popular o banco de dados que está no ar no Render/Aiven pelo seu terminal local:

1. Defina a URL do banco (PowerShell):
   ```powershell
   $env:DATABASE_URL="sua_uri_do_aiven"
   ```
2. Execute o script:
   ```powershell
   python seed_db.py
   ```

---

## ⚠️ Notas
- O script não remove superusuários já criados.
- Se quiser limpar o banco antes de popular, descomente a linha `clear_db()` no final do arquivo `seed_db.py`.

#!/bin/sh

# Espera o banco de dados estar pronto (opcional, mas recomendado)
# sleep 5 

echo "🗄️ Aplicando migrações..."
python manage.py migrate --no-input

echo "🗂️ Coletando arquivos estáticos..."
python manage.py collectstatic --no-input

exec "$@"

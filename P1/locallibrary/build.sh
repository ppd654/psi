#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Instalar las dependencias (librerías)
pip install -r requirements.txt

# 2. Recolectar archivos estáticos (CSS, imágenes) para que se vean en la nube
python manage.py collectstatic --no-input

# 3. Aplicar las migraciones a la base de datos de la nube
python manage.py migrate

# 4. Crear el superusuario automáticamente (usando el comando que creamos antes)
python manage.py createsu
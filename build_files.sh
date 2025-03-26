#!/bin/bash

pip install -r requirements.txt

# Apply database migrations
python3.12 manage.py migrate

# Collect static files
mkdir -p staticfiles
python3.12 manage.py collectstatic --noinput

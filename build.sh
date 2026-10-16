#!/usr/bin/env bash

set -o errexit

python -m pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', '비밀번호1234')"
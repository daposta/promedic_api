#!/usr/bin/env bash

set -e

# TODO: Set to URL of git repo.
PROJECT_GIT_URL='https://github.com/daposta/promedic_api.git'

PROJECT_BASE_PATH='/usr/local/apps/promedic_api'
#VIRTUALENV_BASE_PATH='/usr/local/virtualenvs'

# Set Ubuntu Language
locale-gen en_GB.UTF-8

# Install Python, SQLite and pip
echo "Installing dependencies..."
apt-get update
apt-get install -y python3-dev python3-venv sqlite python-pip supervisor nginx git mysql-server mysql-client python-mysqldb

mkdir -p $PROJECT_BASE_PATH
git clone $PROJECT_GIT_URL $PROJECT_BASE_PATH

# Create virtual environment
mkdir -p $PROJECT_BASE_PATH/env
python3 -m venv $PROJECT_BASE_PATH/env

$PROJECT_BASE_PATH/env/bin/pip install -r $PROJECT_BASE_PATH/src/promedic/requirements.txt
$PROJECT_BASE_PATH/env/bin/pip install gunicorn 

# Run migrations
cd $PROJECT_BASE_PATH/src/promedic
$PROJECT_BASE_PATH/env/bin/python manage.py makemigrations
$PROJECT_BASE_PATH/env/bin/python manage.py migrate
$PROJECT_BASE_PATH/env/bin/python manage.py collectstatic --noinput

# Setup Supervisor to run our uwsgi process.
#rm /etc/supervisor/conf.d/supervisor_passme_api.conf
cp $PROJECT_BASE_PATH/deploy/supervisor_promedic_api.conf /etc/supervisor/conf.d/supervisor_promedic_api.conf
supervisorctl reread
supervisorctl update
supervisorctl restart promedic_api

# Setup nginx to make our application accessible.
#rm /etc/nginx/sites-available/nginx_passme_api.conf /etc/nginx/sites-enabled/nginx_passme_api.conf
cp $PROJECT_BASE_PATH/deploy/nginx_promedic_api.conf /etc/nginx/sites-available/nginx_passme_api.conf
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/nginx_promedic_api.conf /etc/nginx/sites-enabled/nginx_promedic_api.conf
systemctl restart nginx.service

echo "DONE! :)"
# Notes for setting up repository "my_json-reader"

## Repository:
- [https://github.com/oesterli/my_json-reader.git](https://github.com/oesterli/my_json-reader.git)
- create dev branch by running
```bash
git checkout -b develop
```
- in github set `develop` as default branch (Settings > General > Default branch) 

## App

Source: [https://v2.vitejs.dev/guide/#scaffolding-your-first-vite-project](https://v2.vitejs.dev/guide/#scaffolding-your-first-vite-project)

### Commands
- Create vite TS app by running: 
```bash
npm create vite@latest my-json-reader --template lit-ts
```
- run the app:
```bash
cd app/my-json-reader
npm run dev
```

## API

- Set up directory strucutre

### Commands

```bash
cd api
```
- Create python virtual environment
```bash
python3 -m venv venv
```

- Activate venv
```bash
source venv/bin/activate
```

- Install dependencies
```bash
pip install django djangorestframework psycopg2-binary
```

- Install `python-decouple` in order to user environment variables
```bash
pip install python-decouple
``` 

- Save dependencies in requirements.txt
```bash
pip freeze > requirements.txt
```
- Create Django project "config"
```bash
django-admin startproject config .
```

- Create Djangp app "api-app"
```bash
python manage.py startapp api_app
```
- Register App & DRF in `config/settings.py`
```python
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework', # ON: DRF
    'api_app' # ON: api_app
]
```

- Make migrations & run server
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
- Create `.env`-file in Django project root
```bash
cd api
touch .env
```
- Edit `.env`and `setting.py``
```python
# .env
DB_NAME=meinedb
DB_USER=postgres
DB_PASSWORD=meinpasswort123
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=django-geheime-key
DEBUG=True
```

```python
# setting.py
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', cast=int),
    }
}
```
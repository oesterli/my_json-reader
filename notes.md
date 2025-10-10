# Notes for setting up repository "my_json-reader"

## Repsoitory:
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

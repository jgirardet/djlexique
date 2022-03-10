Application Lexique a Lexicon App

### Installation dev
- clone the repo then  `poetry install`
- add a .env file next to manage.py with this content:

```
ALLOWED_HOSTS=127.0.0.1
SECRET_KEY=1
DEBUG=True
```
- `python manage.py migrate`
- `python manage.py createsuperuser`


### Deploy
see deploy.md

### Tech used:

Django
htmx/hyperscrypt
gunicorn
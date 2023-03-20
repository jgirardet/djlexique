# DEPLOY with systemd/gunicorn /nginx/letsenrypts

Simple step by step

## Before Prod

### configure settings

```python
SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = os.environ.get("DEBUG", False)

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(',')  #comma separeted value : myfiresthhist,234.234.234.324,anotherone

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "static"
```

### collect static

```bash
python manage.py collectstatic
```

### add dotenv to wsgi.py

put just after imports :

```python
def read_env():
    import pathlib
    import dotenv
    from django.core.exceptions import ImproperlyConfigured

    envfile = pathlib.Path().parent / ".env"
    if not envfile.exists():
        msg = f"no '.env' file in {envfile.parent.resolve()}"
        print(msg)
        raise ImproperlyConfigured(msg)
    else:
        dotenv.read_dotenv(dotenv=envfile)


read_env()
```

## in Production

### clone repo and set permission

```bash
$ cd /opt
$ sudo git clone https://github.com/jgirardet/djlexique.git
$ sudo chown -R me djlexique
$ cd djlexique
$ python3.8 -m venv .venv
$ source .venv/bin/activate
$ poetry install
```

### add .env file

get the secret key
```bash
python -c 'from django.core.management.utils import get_random_secret_key; \
            print(get_random_secret_key())'
```
add .env file next manage.py
`vi .env`
```env
SECRET_KEY=thesecretkey
ALLOWED_HOSTS="lexique.myhost.com"
```

### initialise django et fix permissions
```
$ python manage.py migrate
$ python manage.py createsuperuser
$ cd /opt
$ sudo chown -R me:www-data djlexique
$ deactivate
```

### add systemd serviec
add file `sudo vi /etc/systemd/system/djlexique.service`

```
[Unit]
Description=djlexique daemon
After=network.target
[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/djlexique/djlexique
StandardOutput=journal+console
ExecStart=/opt/djlexique/.venv/bin/gunicorn  --workers 3 --bind unix:/opt/djlexique/djlexique.sock djlexique.wsgi:application
[Install]
WantedBy=multi-user.target
```

```bash
$ sudo systemctl daemon-reload
$ sudo systemctl enable djlexique.service
$ sudo systemctl start djlexique.service
$ sudo systemctl status djlexique.service #simple check
```

### configure NGINX

create `/etc/nginx/sites-avalaible/lexique`
add
```
server { 
    server_name lexique.myhost.com; 
    location = /favicon.ico { access_log off; log_not_found off; } 
    location /static/ { 
        root /opt/djlexique/djlexique/;tail  
    } 
    location / { 
        include proxy_params; 
        proxy_pass http://unix:/opt/djlexique/djlexique.sock; 
    } 
}
```

Activate
```
$ sudo ln -s /etc/nginx/sites-available/lexique /etc/nginx/sites-enabled/lexique
$ sudo systemctl restart nginx
```

Test the site

### Add Https to nginx

Install certbot : `https://certbot.eff.org/`
or just run certbot if already installed : `sudo certbot --nginx`


## Update un Production
```bash
$ git pull
$ source .venv/bin/activate
$ poetry update
$ sav ddb si migration
$ python manage.py migrate # if needed
$ deactivate
$ sudo chown -R me:www-data /opt/djlexique
$ sudo sytemctl restart djlexique.service
```




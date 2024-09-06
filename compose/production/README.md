# Userquery Production Installation

Copy files and create directories

```bash
git clone https://github.com/linea-it/lsp_daiquiri.git userquery-temp \
&& cp -r userquery-temp/compose/production userquery \
&& rm -rf userquery-temp \
&& cd userquery \
&& mkdir -p data data/download data/files data/upload logs certificates \
&& chmod -R g+w data logs \
&& mv env_template .env
```

Generate SAML2 Certificates

```bash
cd certificates \
&& openssl genrsa -out mykey.key 2048 \
&& openssl req -new -key mykey.key -out mycert.csr \
&& openssl x509 -req -days 365 -in mycert.csr -signkey mykey.key -out mycert.crt \
&& cp mykey.key mykey.pem \
&& cp mycert.crt mycert.pem \
&& cd ..
```

Edit .env for secrets, users and passwords.

Run backend first time and generate a secret for Django.

```bash
docker compose exec -it backend python -c "import secrets; print(secrets.token_urlsafe())"
```


```bash
docker compose exec backend python manage.py loaddata /app/fixtures/initial_data.json
```

```bash
docker compose exec backend python manage.py loaddata /app/fixtures/query_samples.json
```

```bash
docker compose exec backend python manage.py setup_groups
```

```bash
docker compose exec backend python manage.py setup_tap_metadata
```

```bash
docker compose exec backend python manage.py createsuperuser
```

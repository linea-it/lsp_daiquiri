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

```bash
docker compose up backend
```
CRTL+C

Executar os container em background para proceguir com a instalação
```bash
docker compose up -d
```

Run first time and generate a secret for Django.

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

É necessário reinicar os serviços.

```bash
docker compose stop && docker compose up -d
```

## Registro de Catalogos/Tabelas

É necessário acesar a interface administrativa para registrar os metadados das tabelas de catalogos.
Este processo deve ser feito para cada um schema de catalogo [des_dr2, gaia_dr3, twomass]

1. fazer login no adm do django https://userquery.linea.org.br/admin/
2. voltar para a home https://userquery.linea.org.br
3. acessar o menu "Management" -> "Metadata Management"
4. Clicar em "Create new schema entry"
5. no formulário preencher
    - campo Name ex: des_dr2
    - Access Level: Public
    - Metadata Access Level: Public
    - Verificar se a opção "Automatically discover tables and columns" está marcada.
6. Clicar em Save.
7. atualizar a janela.
8. ir no terminal e importar os metadados utilizando o comando do django `update_table_metadata`. passando o nome do schema como parametro
```bash
    docker compose exec backend python manage.py update_table_metadata des_dr2
```

Este processo deve ser repetido para cada um dos schemas de catalogos. [des_dr2, gaia_dr3, twomass]

Abaixo algumas imagens do processo de registro.

![Step 1](https://github.com/linea-it/lsp_daiquiri/blob/master/docs/metadata_1.jpg)

![Step 2](https://github.com/linea-it/lsp_daiquiri/blob/master/docs/metadata_2.jpg)

![Step 3](https://github.com/linea-it/lsp_daiquiri/blob/master/docs/metadata_3.jpg)

![Step 4](https://github.com/linea-it/lsp_daiquiri/blob/master/docs/metadata_4.jpg)

![Step 5](https://github.com/linea-it/lsp_daiquiri/blob/master/docs/metadata_5.jpg)

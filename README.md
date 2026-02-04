# LIneA User Query (Development)

This application is meant to be used with the Django version of the [Daiquiri Framework](https://github.com/aipescience/django-daiquiri).

>This project is currently in an early stage of development and by no means production ready.

## Requirements

- Docker version 25.0.1
- git version 2.39.3
- Vscode + devcontainer extension
- Acesso ao banco de dados desdb4 - **prod_gavo**

## Docs

- **Daiquiri Docs:** <https://django-daiquiri.github.io/docs>
- **Daiquiri Instalation**: <https://django-daiquiri.github.io/docs/installation/>
- **Daiquiri Framework:** <https://github.com/django-daiquiri/daiquiri>
- **Daiquiri App:** <https://github.com/django-daiquiri/app>
- **GAIA@AIP:** <https://gaia.aip.de/>
- **MUSE-Wide:** <https://musewide.aip.de/>
- **GAIA How to API access**: <https://gaia.aip.de/cms/services/scripted-access/>

## Setup Development Environment
https://github.com/linea-it/lsp_daiquiri/blob/master/compose/local/README.md

## Setup Production Environment
https://github.com/linea-it/lsp_daiquiri/blob/master/compose/production/README.md


### Build Manual da Imagem docker

Estando logado no dockerhub pelo terminal execute o build e o push da imagem do daiquiri.

Docker Hub: <https://hub.docker.com/repository/docker/linea/lsp_daiquiri/>

A identificação unica de cada imagem pode ser o numero de versão exemplo: `linea/lsp_daiquiri:v0.1` ou o hash do commit para versões de desenvolvimento: `linea/lsp_daiquiri:8816330`.

>Para obter o hash do commit usar o comando `$(git describe --always)`

```bash
docker build -f compose/local/daiquiri/Dockerfile -t linea/lsp_daiquiri:$(git describe --always) .
```

```bash
docker push linea/lsp_daiquiri:$(git describe --always)
```


ARG BUILD_ENVIRONMENT=local

FROM python:3.9-slim-bullseye as base

ARG BUILD_ENVIRONMENT
ARG USERNAME=daiquiri
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# If this is set to a non-empty string, Python won’t try
# to write .pyc files on the import of source modules
ENV PYTHONDONTWRITEBYTECODE=1

# Force the stdout and stderr streams to be unbuffered.
# This option has no effect on the stdin stream.
ENV PYTHONUNBUFFERED=1

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    build-essential \
    libxml2-dev \
    libxslt-dev \
    zlib1g-dev \
    libpq-dev \
    python3-dev \
    postgresql-client-13 \
    libsasl2-dev \
    libldap2-dev \
    libssl-dev \
    ldap-utils \
    xmlsec1 \
    git \
    zsh \
    wget \
    vim

# Install python packages
# Create Python Dependency and Sub-Dependency.
COPY ./requirements /tmp/pip-tmp/
RUN pip install --upgrade pip setuptools wheel  && \
    pip --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/$BUILD_ENVIRONMENT.txt \
    && rm -rf /tmp/pip-tmp

FROM base as daiquiri-local
# Install Github CLI
# https://github.com/cli/cli/blob/trunk/docs/install_linux.md
RUN mkdir -p -m 755 /etc/apt/keyrings && wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg | tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
    && chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt update \
    && apt install gh -y

# Install ACT
# https://lindevs.com/install-act-on-ubuntu
RUN wget -qO act.tar.gz https://github.com/nektos/act/releases/latest/download/act_Linux_x86_64.tar.gz \
    && tar xf act.tar.gz -C /usr/local/bin act \
    && act --version \
    && rm -rf act.tar.gz

FROM base as daiquiri-production


FROM daiquiri-$BUILD_ENVIRONMENT

ENV PATH="/home/daiquiri/.local/bin:$PATH"

# FIX: django-shibboleth-remoteuser Incompativel com Vesão 4.x do Django.
COPY ./shibboleth/urls.py /usr/local/lib/python3.9/site-packages/shibboleth/urls.py

# Create the non-root user up front
RUN groupadd --gid ${USER_GID} $USERNAME \
    && useradd --uid ${USER_UID} --gid ${USER_GID} -m ${USERNAME} \
    && mkdir -p /app /data /celery /var/run/celery /var/log/daiquiri/ /workspaces \
    && chown -R ${USER_UID}:${USER_GID} /app /data /celery /var/run/celery /var/log/daiquiri/ /workspaces \
    && chmod -R g+w /app /data /celery /var/run/celery /var/log/daiquiri/ /workspaces

# Copy app files into container
WORKDIR /app
COPY ./daiquiri /app

# Basic Settings necessary for run download_vendor_files during build process
# NÃO ALTERAR os paths utilizar os volumes no docker-compose para indicar os diretórios.
ENV LOG_DIR=/var/log/daiquiri/
ENV FILES_BASE_PATH=/data/download
ENV FILES_BASE_URL=/download
ENV QUERY_DOWNLOAD_DIR=/data/download
ENV QUERY_UPLOAD_DIR=/data/upload
ENV ARCHIVE_BASE_PATH=/data/download
ENV ARCHIVE_DOWNLOAD_DIR=/data/download

COPY --chmod=0755 ./compose/local/daiquiri/entrypoint.sh /entrypoint.sh
COPY --chmod=0755 ./compose/local/daiquiri/start.sh /start.sh


USER $USERNAME


# Install Oh My Zsh
RUN sh -c "$(wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O -)" --unattended

ENTRYPOINT [ "/entrypoint.sh" ]

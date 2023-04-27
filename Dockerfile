FROM python:3.9-slim-bullseye as builder

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
    git

# Install python packages
COPY ./requirements.txt /tmp/pip-tmp/
RUN pip install --upgrade pip setuptools wheel  && \
    pip --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp

ENV PATH="/home/daiquiri/.local/bin:$PATH"

# Create the non-root user up front
ARG USERNAME=daiquiri
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid ${USER_GID} $USERNAME \
    && useradd --uid ${USER_UID} --gid ${USER_GID} -m ${USERNAME} \
    && mkdir -p /app /data \
    && chown -R ${USER_UID}:${USER_GID} /app \
    && chown -R ${USER_UID}:${USER_GID} /data

# Copy app files into container
WORKDIR /app
COPY ./daiquiri /app

# Basic Settings necessary for run download_vendor_files during build process
# NÃO ALTERAR os paths utilizar os volumes no docker-compose para indicar os diretórios.
ENV FILES_BASE_PATH=/data/files
ENV QUERY_DOWNLOAD_DIR=/data/download
ENV QUERY_UPLOAD_DIR=/data/upload
ENV ARCHIVE_BASE_PATH=/data/files
ENV ARCHIVE_DOWNLOAD_DIR=/data/download

COPY --chmod=0755 ./entrypoint.sh /entrypoint.sh
COPY --chmod=0755 ./start.sh /start.sh

USER $USERNAME

ENTRYPOINT [ "/entrypoint.sh" ]

FROM mcr.microsoft.com/devcontainers/python:0-3.9

# If this is set to a non-empty string, Python won’t try
# to write .pyc files on the import of source modules
ENV PYTHONDONTWRITEBYTECODE=1

# Force the stdout and stderr streams to be unbuffered.
# This option has no effect on the stdin stream.
ENV PYTHONUNBUFFERED=1

# [Optional] Uncomment this section to install additional OS packages.
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

# Install python Development packages
COPY ./requirements-dev.txt /tmp/pip-tmp/
RUN pip install --upgrade pip setuptools wheel  && \
    pip --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements-dev.txt \
    && rm -rf /tmp/pip-tmp

# Install python packages
COPY ./requirements.txt /tmp/pip-tmp/
RUN pip install --upgrade pip setuptools wheel  && \
    pip --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp


COPY --chmod=0755 ./entrypoint.sh /entrypoint.sh
COPY --chmod=0755 ./start.sh /start.sh

ENTRYPOINT [ "/entrypoint.sh" ]

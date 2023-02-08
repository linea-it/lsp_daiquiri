FROM python:3.9-bullseye as builder

# If this is set to a non-empty string, Python won’t try
# to write .pyc files on the import of source modules
ENV PYTHONDONTWRITEBYTECODE=1

# Force the stdout and stderr streams to be unbuffered.
# This option has no effect on the stdin stream.
ENV PYTHONUNBUFFERED=1

ARG USERNAME=daiquiri
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY requirements.txt .

# Install postgresql client
# RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
#     && sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'

# this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends \ 
#     build-essential \
#     libxml2-dev libxslt-dev \
#     zlib1g-dev \
#     libssl-dev \
#     python3-dev \
#     libpq-dev \
#     postgresql-client

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \ 
    build-essential \
    libxml2-dev libxslt-dev \
    zlib1g-dev \
    libssl-dev \
    python3-dev \
    libpq-dev \
    postgresql-client-13


RUN pip3 install --upgrade pip setuptools wheel  && \
    pip3 --disable-pip-version-check --no-cache-dir install -r requirements.txt \
    && rm -rf /tmp/pip-tmp


# FROM python:3.10-slim

# COPY --from=builder /usr/lib/x86_64-linux-gnu /usr/lib/x86_64-linux-gnu
# COPY --from=builder /opt/venv /opt/venv

# WORKDIR /app

# ENV PATH="/opt/venv/bin:$PATH"
# add user so we can run things as non-root
# RUN useradd -m -d /app -c "Daiquiri user" -s /bin/bash daiquiri
RUN groupadd --gid $USER_GID $USERNAME
RUN useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME

COPY ./entrypoint.sh .

COPY . .

USER $USERNAME

ENTRYPOINT ./entrypoint.sh
FROM python:3.9-bullseye as builder

# If this is set to a non-empty string, Python won’t try
# to write .pyc files on the import of source modules
ENV PYTHONDONTWRITEBYTECODE=1

# Force the stdout and stderr streams to be unbuffered.
# This option has no effect on the stdin stream.
ENV PYTHONUNBUFFERED=1

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN pip3 --disable-pip-version-check --no-cache-dir install -r requirements.txt \
    && rm -rf /tmp/pip-tmp

WORKDIR /app

# FROM python:3.10-slim

# COPY --from=builder /usr/lib/x86_64-linux-gnu /usr/lib/x86_64-linux-gnu
# COPY --from=builder /opt/venv /opt/venv

# WORKDIR /app

# ENV PATH="/opt/venv/bin:$PATH"

COPY ./entrypoint.sh /app/entrypoint.sh

COPY . /app

CMD ./entrypoint.sh
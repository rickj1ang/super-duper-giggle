FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    TZ=America/New_York \
    LANG=en_US.UTF-8

WORKDIR /app

# System deps: fonts and basics
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       curl ca-certificates \
       fonts-dejavu fonts-liberation fonts-noto \
       locales \
    && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY src /app/src
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENV PYTHONPATH=/app/src

ENTRYPOINT ["/app/entrypoint.sh"]



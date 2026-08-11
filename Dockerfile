ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim

ARG DJANGO_VERSION=5.2
ARG PKG_SPEC="django-silk"

RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir "Django==${DJANGO_VERSION}" ${PKG_SPEC}

WORKDIR /app
COPY app/ /app/
COPY entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

ENV PYTHONUNBUFFERED=1
EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]

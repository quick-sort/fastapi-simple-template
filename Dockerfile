from python:3.12-alpine
WORKDIR /app
ENV PYTHONPATH=/app
ENV PYCURL_SSL_LIBRARY=openssl
ENV TZ=Asia/Shanghai

ADD pyproject.toml /app/pyproject.toml

RUN cd /app && \
    apk update && \
    apk add --no-cache libcurl curl && \
    apk add --no-cache --virtual .build-deps build-base curl-dev && \
    pip install --no-cache-dir pycurl poetry && \
    POETRY_VIRTUALENVS_CREATE=false poetry install --no-root && \
    pip uninstall -y poetry && \
    apk del .build-deps

ADD . /app

EXPOSE 8000
HEALTHCHECK CMD curl --fail http://localhost:8000/api/health/ping

CMD ["sh", "-c", "alembic upgrade head; uvicorn app.main:app --host 0.0.0.0 --port 8000"]

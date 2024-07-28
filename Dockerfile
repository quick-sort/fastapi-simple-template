from python:3.12-alpine
WORKDIR /app
ENV PYTHONPATH=/app

RUN apk update && \
    apk add build-base curl && \
    pip install poetry

ADD . /app

RUN cd /app && \
    POETRY_VIRTUALENVS_CREATE=false poetry install --no-root

EXPOSE 8000
HEALTHCHECK CMD curl --fail http://localhost:8000/docs/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

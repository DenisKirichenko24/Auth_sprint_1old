FROM python:3.8-slim-buster

WORKDIR /app

RUN python3 -m venv /opt/venv

COPY ./requirements.txt ./

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=api/main.py
ENV FLASK_DEBUG=1
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

RUN . /opt/venv/bin/activate && pip install --upgrade pip --no-cache-dir  \
    && pip install -r requirements.txt --no-cache-dir && pip uninstall jwt -y && pip uninstall PyJWT -y && pip install PyJWT

COPY api ./

EXPOSE 8000/tcp

CMD . /opt/venv/bin/activate && gunicorn --bind 0.0.0.0:8000 main:app


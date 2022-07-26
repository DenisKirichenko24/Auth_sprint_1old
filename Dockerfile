FROM python:3.8-slim-buster

WORKDIR /app

COPY ./requirements.txt ./

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=main.py
ENV FLASK_DEBUG=1
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

COPY api ./

RUN pip install --upgrade pip --no-cache-dir && pip install -r requirements.txt --no-cache-dir


CMD ["python", "-m", "flask", "run"]

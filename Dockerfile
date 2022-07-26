FROM python:3.10-bullseye

WORKDIR /app

COPY ./requirements.txt ./

COPY api ./
RUN pip3 install --upgrade pip --no-cache-dir && pip3 install -r requirements.txt --no-cache-dir


CMD ["gunicorn --bind 0.0.0.0:5001 main:app"]

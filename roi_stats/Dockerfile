FROM python:latest
#RUN apk update && apk add gcc libc-dev
RUN mkdir /app
COPY requirements.txt /app

RUN pip3 install --upgrade pip
RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY . /app
WORKDIR /app

ENV PRODUCTION=1

CMD gunicorn --workers 2 --bind 0.0.0.0:8000 roi_stats.wsgi:application
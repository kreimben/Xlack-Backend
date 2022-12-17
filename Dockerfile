FROM python:3.11-bullseye

WORKDIR app

COPY . /app

EXPOSE 8000

RUN apt-get update && \
    apt-get -y upgrade && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "xlack.asgi:application", "-v", "3"]
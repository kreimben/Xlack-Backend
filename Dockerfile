FROM python

WORKDIR app

COPY . /app

EXPOSE 8000

RUN apt-get update && \
    apt-get -y upgrade && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

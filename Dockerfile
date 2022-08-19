FROM python:3.10.5-bullseye

WORKDIR app

COPY . /app

EXPOSE 8000

RUN apt-get update && \
    apt-get -y upgrade && \
    pip install --upgrade pip && \
    pip install -r /requirements.txt

RUN python manage.py collectstatic -v 2 --noinput

#CMD ["gunicorn", "xlack.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0", "-p", "8000"]
#CMD ["gunicorn", "xlack.wsgi"]
#CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "xlack.asgi:application"]
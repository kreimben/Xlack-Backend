FROM python:3.10.5-bullseye

WORKDIR app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

#CMD ["gunicorn", "xlack.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0", "-p", "8000"]
#CMD ["gunicorn", "xlack.wsgi"]
#CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "xlack.asgi:application"]
FROM python:3.10.5-bullseye

WORKDIR app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 10131
EXPOSE 8000

#ENTRYPOINT ["daphne", "-b", "0.0.0.0", "-p", "8000", "xlack.asgi:application"]
#ENTRYPOINT gunicorn xlack.asgi:application -k uvicorn.workers.UvicornWorker
CMD ["uvicorn", "xlack.asgi:application", "--port", "8000", "--host", "0.0.0.0"]
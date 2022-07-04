FROM python:3.10.5-bullseye

WORKDIR app

COPY . /app

RUN pip install -r requirements.txt
RUN ls -hal /app

EXPOSE 10131

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
FROM python:3.10.5-bullseye

WORKDIR app

COPY . .

EXPOSE 10131

RUN pip install -r requirements.txt

CMD ["python /app/main.py"]
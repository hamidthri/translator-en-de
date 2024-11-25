FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV TELEGRAM_BOT_TOKEN="type your token"

CMD ["python", "translate.py"]

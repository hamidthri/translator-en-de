FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV TELEGRAM_BOT_TOKEN=7035003859:AAEjfFEqNhkHV6gqmjO5_krljhpTFWUTiXs

CMD ["python", "translate.py"]

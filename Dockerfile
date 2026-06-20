FROM python:3.10-slim

WORKDIR /app

# Serverga eng kerakli paketlarni oldindan o'rnatamiz
RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]

FROM python:3.10-alpine

WORKDIR /app

COPY app.py /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY .env .env

CMD ["python", "app.py"]
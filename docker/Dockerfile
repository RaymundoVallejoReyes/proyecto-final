# Etapa 1: builder
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Etapa 2: imagen final
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /install /usr/local
COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]

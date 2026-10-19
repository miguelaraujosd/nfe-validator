FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app/src

# Comando padrão: roda o harness de testes com relatório de cobertura
CMD ["pytest", "-v", "--cov=src/nfe_validator", "--cov-report=term-missing"]

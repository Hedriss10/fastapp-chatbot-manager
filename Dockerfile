# Imagem base leve
FROM python:3.12-slim

# Diretório de trabalho
WORKDIR /app

# Dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiar código do projeto
COPY app app
COPY app/main.py .

# Copiar pasta static (pode estar vazia, evita erro)
RUN mkdir -p /app/app/static

# Expor porta FastAPI
EXPOSE 8000

# Rodar produção com uvicorn (4 workers)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

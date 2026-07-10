FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY pyproject.toml .
RUN pip install -e .

RUN useradd -m -u 1000 giftos && chown -R giftos:giftos /app
USER giftos

EXPOSE 8000

CMD ["uvicorn", "giftos.main:app", "--host", "0.0.0.0", "--port", "8000"]

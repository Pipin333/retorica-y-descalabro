# Dockerfile multi-stage para FastAPI
FROM python:3.13-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Runner stage
FROM python:3.13-slim AS runner

WORKDIR /app

RUN useradd -m -u 1000 appuser

COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . .

ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/languages')" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

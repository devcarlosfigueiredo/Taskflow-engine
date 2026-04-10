# ──────────────────────────────────────────────
# Stage 1 — Builder: instala dependências
# ──────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /install

# Copia apenas o requirements para aproveitar cache de camadas
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --prefix=/install/deps --no-cache-dir -r requirements.txt


# ──────────────────────────────────────────────
# Stage 2 — Runtime: imagem final enxuta
# ──────────────────────────────────────────────
FROM python:3.12-slim AS runtime

# Metadados da imagem
LABEL maintainer="seu-usuario@email.com"
LABEL description="TaskFlow API — Projeto CI/CD de portfólio"
LABEL version="1.0.0"

# Variáveis de ambiente padrão
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000 \
    FLASK_DEBUG=false \
    APP_VERSION=1.0.0

WORKDIR /app

# Copia as dependências instaladas no stage builder
COPY --from=builder /install/deps /usr/local

# Copia apenas o código da aplicação
COPY src/ ./src/

# Cria usuário não-root para segurança
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser
USER appuser

# Expõe a porta da aplicação
EXPOSE 5000

# Health check nativo do Docker
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/')" || exit 1

# Comando de inicialização
CMD ["python", "src/app.py"]

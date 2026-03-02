# -------------------------------------------------------------------
# STAGE 1: Builder
# Compila todas as dependências num ambiente efêmero para reduzir tamanho
# -------------------------------------------------------------------
FROM python:3.11-slim as builder

# Define variáveis de ambiente pro Python não gerar arquivo pyc e logs não ficarem no buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /install

# Instala as ferramentas de build necessárias pro psycopg2 e afins
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Instala via pip ignorando o cache para poupar espaço final da imagem
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# -------------------------------------------------------------------
# STAGE 2: Runtime
# Imagem pura gerada apenas com o código, sem o GCC/Build Tools. Segura e Leve.
# -------------------------------------------------------------------
FROM python:3.11-slim as runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production

# Instala apenas as dependências vitais de execução pro postgres
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Cria o diretório da app e seta para o superusuário root
WORKDIR /app

# Regra de Ouro Security / Rootless Container:
# Cria um grupo e um usuário de sistema sem privilégios. App não rodará com UID 0 (root).
RUN addgroup --system appgroup && adduser --system --group appuser
RUN chown -R appuser:appgroup /app

# Copia os pacotes compilados na etapa Build (Sem trazer as dependências pesadas extras)
COPY --from=builder /install /usr/local

# Copia todo o código-fonte
COPY . /app

# Troca do root pelo usuário criado para proteger de ataques Privelege Escalation (CVEs)
USER appuser

# Exclui .git e afins do container (será feito via .dockerignore tbm)
# Expondo a porta correta pro Gunicorn
EXPOSE 8000

# Execução baseada em Performance: Gunicorn como Gerenciador do Uvicorn (Arquitetura ASGI de Múltiplos Workers)
# -w 4 -> Pode ser adaptado via Variavel de Ambiente
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "-b", "0.0.0.0:8000"]

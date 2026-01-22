# ============================================
# STAGE 1: Builder - Instala dependências
# ============================================
FROM python:3.12-slim AS builder

WORKDIR /build

# Instala dependências de build necessárias
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Cria virtualenv para isolar dependências
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copia e instala dependências (aproveita cache do Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt


# ============================================
# STAGE 2: Runtime - Imagem final mínima
# ============================================
FROM python:3.12-slim AS runtime

ARG APP_PATH=/usr/src/app
WORKDIR ${APP_PATH}

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# Instala apenas dependências runtime mínimas + locale
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    locales \
    libpq5 \
 && sed -i '/pt_BR.UTF-8/s/^# //g' /etc/locale.gen \
 && locale-gen \
 && apt-get purge -y --auto-remove \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Locale envs
ENV LANG=pt_BR.UTF-8 \
    LANGUAGE=pt_BR:en \
    LC_ALL=pt_BR.UTF-8

# Cria usuário não-root
RUN groupadd -g 1000 app_user \
 && useradd -u 1000 -ms /bin/bash -g app_user app_user

# Copia virtualenv do stage builder
COPY --from=builder /opt/venv /opt/venv

# Copia código da aplicação
COPY --chown=app_user:app_user . ${APP_PATH}

# Troca para usuário não-root
USER app_user

ENV FLASK_RUN_PORT=8000 \
    ENV_FOR_DYNACONF=production \
    ROOT_PATH_FOR_DYNACONF=/usr/src/app \
    SETTINGS_FILES_FOR_DYNACONF=/usr/src/app/settings.toml \
    FLASK_APP=nuBox/app.py

EXPOSE 8000

# Usa gunicorn em produção para melhor performance
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "nuBox.app:create_app()"]


# ============================================
# STAGE 3: Development - Com ferramentas de dev
# ============================================
FROM runtime AS development

USER root

# Instala dependências de desenvolvimento
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

USER app_user

ENV FLASK_DEBUG=1 \
    ENV_FOR_DYNACONF=development

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]

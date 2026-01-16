# Força imagem moderna (Debian bookworm)
FROM python:3.12-slim

ARG CACHE_BUST=20260116

ARG APP_PATH=/usr/src/app
WORKDIR ${APP_PATH}

ENV DEBIAN_FRONTEND=noninteractive

# ---- Instala dependências do sistema + locale correto ----
RUN apt update \
 && apt install -y --no-install-recommends \
    locales \
    ca-certificates \
 && sed -i '/pt_BR.UTF-8/s/^# //g' /etc/locale.gen \
 && locale-gen \
 && rm -rf /var/lib/apt/lists/*

# ---- Locale envs ----
ENV LANG=pt_BR.UTF-8 \
    LANGUAGE=pt_BR:en \
    LC_ALL=pt_BR.UTF-8

# ---- Cria usuário não-root ----
RUN groupadd -g 1000 app_user \
 && useradd -u 1000 -ms /bin/bash -g app_user app_user

COPY requirements.txt requirements-dev.txt ./

RUN pip install --no-cache-dir -r requirements-dev.txt

# ---- Copia código com owner correto ----
COPY --chown=app_user:app_user . ${APP_PATH}

RUN chmod -R 755 ${APP_PATH}

# ---- Troca para usuário não-root ----
USER app_user

ENV FLASK_RUN_PORT=8000 \
    FLASK_DEBUG=1 \
    ENV_FOR_DYNACONF=development \
    FLASK_APP=nuBox/app.py

EXPOSE 8000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]

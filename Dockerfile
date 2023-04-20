FROM python:3.7.3

ARG APP_PATH='/usr/src/app'

WORKDIR $APP_PATH

COPY requirements.txt .
# Set the locale to money currency formatation
RUN apt-get -y update && apt-get -y install locales locales-all
ENV LANG pt_BR.UTF-8  
ENV LANGUAGE pt_BR:en  
ENV LC_ALL pt_BR.UTF-8 

# Add user 
RUN groupadd -g 1000 app_user
RUN useradd -u 1000 -ms /bin/bash -g app_user app_user

# Copy existing application directory permissions
COPY --chown=app_user:app_user . $APP_PATH

RUN chown app_user:app_user -R $APP_PATH
RUN chmod 777 -R $APP_PATH
RUN chmod g+s -R  $APP_PATH

# Change current user to app_user
USER app_user 

# RUN python -m venv .venv && source .venv/bin/activate
RUN pip install -r requirements-dev.txt --user 

ENV FLASK_RUN_PORT=8000
ENV FLASK_DEBUG=1
ENV ENV_FOR_DYNACONF=development
ENV FLASK_APP=nuBox/app.py

CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0"]

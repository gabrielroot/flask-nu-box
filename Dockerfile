FROM python:3.7.3

ARG APP_PATH='/usr/src/app'

WORKDIR $APP_PATH

COPY requirements.txt .

# Add user 
RUN groupadd -g 1000 app_user
RUN useradd -u 1000 -ms /bin/bash -g app_user app_user

RUN pip install -r requirements.txt

ENV FLASK_RUN_PORT=8000
ENV FLASK_APP=projetoFlask/app.py
ENV FLASK_DEBUG=1

# Set the locale to money currency formatation
RUN apt-get -y update && apt-get -y install locales locales-all
ENV LANG pt_BR.UTF-8  
ENV LANGUAGE pt_BR:en  
ENV LC_ALL pt_BR.UTF-8     


CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0"]

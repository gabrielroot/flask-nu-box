from flask import render_template, flash
from flask_login import login_required
from projetoFlask.blueprints.webui.services import flashMessagesService

@login_required
def index():
    flashMessagesService.addSuccessMessage('Testando flashMessages')
    return render_template("dashboard.html")
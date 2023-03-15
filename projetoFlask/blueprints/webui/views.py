from flask import abort, render_template
from flask_login import login_required, current_user
from projetoFlask.ext.database import Product

@login_required
def index():
    return render_template("dashboard.html")

@login_required
def myBoxes():
    return render_template("boxes/index.html")

@login_required
def movimentations():
    return render_template("movimentations/index.html")

@login_required
def profile():
    return render_template("user/profile.html", username=current_user.username)
from flask import render_template
from flask_login import login_required


@login_required
def myBoxes():
    return render_template("boxes/index.html")
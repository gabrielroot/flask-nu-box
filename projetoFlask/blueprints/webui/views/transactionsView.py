from flask import abort, render_template
from flask_login import login_required


@login_required
def transactions():
    return render_template("transactions/index.html")
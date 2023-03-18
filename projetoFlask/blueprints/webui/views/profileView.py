from flask import render_template
from flask_login import login_required, current_user


@login_required
def profile():
    return render_template("user/profile.html", username=current_user.username)
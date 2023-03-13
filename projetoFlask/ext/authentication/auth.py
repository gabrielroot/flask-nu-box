from projetoFlask.ext.database import db, User
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, render_template, redirect, url_for, request, flash


def create_user(username, password):
    if User.query.filter_by(username=username).first():
        raise RuntimeError(f'{username} já está cadastrado')
    user = User(username=username, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return user

def login():
    return render_template("login.html")

def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    
    login_user(user, remember=remember)
    return redirect(url_for('auth.profile'))

def signup():
    return render_template("signup.html")

def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first() 

    if user:
        flash(f'O nome de usuário "{username}" já está cadastrado.')
        return redirect(url_for('auth.signup'))

    new_user = User(username=username, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@login_required
def logout():
    logout_user()
    return redirect(url_for('webui.index'))

@login_required
def profile():
    return render_template("profile.html", username=current_user.username)

#Auth
bpAuth = Blueprint("auth", __name__, template_folder="templates", url_prefix="/auth")

bpAuth.add_url_rule('/login', view_func=login)
bpAuth.add_url_rule('/login', view_func=login_post, methods=['POST'])
bpAuth.add_url_rule('/signup', view_func=signup)
bpAuth.add_url_rule('/signup', view_func=signup_post, methods=['POST'])
bpAuth.add_url_rule('/logout', view_func=logout)

bpAuth.add_url_rule('/profile', view_func=profile)

def init_app(app):
    app.register_blueprint(bpAuth)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
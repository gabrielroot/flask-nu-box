from projetoFlask.ext.database import db, User
from flask_login import login_user, login_required, logout_user
from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import check_password_hash, generate_password_hash


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
        flash('Nome de usuário ou senha inválidos.')
        return redirect(url_for('auth.login'))
    
    login_user(user, remember=remember)
    return redirect(url_for('webui.index'))


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
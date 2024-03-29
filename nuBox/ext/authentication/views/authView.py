from flask import request, url_for, redirect, render_template
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

from nuBox.ext.database import User, Balance
from nuBox.blueprints.webui.services import flashMessagesService


def create_user(username, password):
    if User.query.filter_by(username=username).first():
        raise RuntimeError(f'{username} já está cadastrado')

    balance = Balance(total=0)
    user = User(username=username, password=generate_password_hash(password, method='sha256'), balance=balance)
    user.persist()

    return user


def login():
    return render_template("login.html")


def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username, deleted=False).first()

    if not user or not check_password_hash(user.password, password):
        flashMessagesService.addErrorMessage('Nome de usuário ou senha inválidos.')
        return redirect(url_for('auth.login'))

    flashMessagesService.addSuccessMessage(f"Bem-vindo(a) de volta {username}!")
    login_user(user, remember=remember)
    return redirect(url_for('webui.index'))


def signup():
    return render_template("signup.html")


def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')

    try:
        create_user(username=username, password=password)
    except RuntimeError:
        flashMessagesService.addWarningMessage(f'Nome de usuário "{username}" não disponível.')
        return redirect(url_for('auth.signup'))

    flashMessagesService.addSuccessMessage(f'O usuário "{username}" foi criado com sucesso!')
    return redirect(url_for('auth.login'))


@login_required
def logout():
    logout_user()
    return redirect(url_for('webui.index'))

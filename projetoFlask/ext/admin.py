from flask_admin import Admin, BaseView, expose
from flask_simplelogin import is_logged_in
from flask import redirect, url_for
from flask_admin.contrib import sqla
from flask_admin.base import AdminIndexView
from flask_simplelogin import login_required
from werkzeug.security import generate_password_hash

from projetoFlask.ext.database import db, Product, User
#from projetoFlask.models import Product, User

# Proteger o admin com login via Monkey Patch
AdminIndexView._handle_view = login_required(AdminIndexView._handle_view)
sqla.ModelView._handle_view = login_required(sqla.ModelView._handle_view)
admin = Admin()


class UserAdmin(sqla.ModelView):
    column_list = ['username']
    can_edit = True

    def is_accessible(self):
        return is_logged_in()

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/login')

    def on_model_change(self, form, model, is_created):
        model.password = generate_password_hash(model.password)

class ProductAdmin(sqla.ModelView):
    column_list = ['name', 'price', 'description']
    can_edit = True

    def is_accessible(self):
        return is_logged_in()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

#cusrom Nav item
class AnalyticsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')

def init_app(app):
    admin.name = app.config.TITLE
    admin.template_mode = "bootstrap3"
    admin.init_app(app)
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(ProductAdmin(Product, db.session))
    admin.add_view(AnalyticsView(name='Analytics', endpoint='analytics'))

from flask_admin import Admin
from flask_admin.base import AdminIndexView
from flask_admin.contrib import sqla
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from flask import redirect, url_for
from application.ext.database import db
from application.models import User


# Proteger o admin com login via Monkey Patch
#AdminIndexView._handle_view = login_required(AdminIndexView._handle_view)
sqla.ModelView._handle_view = login_required(sqla.ModelView._handle_view)

class MyAdminViews(AdminIndexView):
    
    def _handle_view(self, name, **kwargs):
        return super()._handle_view(name, **kwargs)
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    
    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('admin_secury.admin_login'))

admin = Admin(name='batata',index_view=MyAdminViews(url='/admin',endpoint='admin'))

def format_user_name(view, context, model, name):
    return model.username.split('@')[0].upper()

class UserView(sqla.ModelView):
    column_list = ['username']
    column_formatters = {'username':format_user_name}
    can_edit = True

    def on_model_change(self, form, model, is_created):
        model.password = generate_password_hash(model.password)
    def get_query(self):
      return self.session.query(self.model).filter(self.model.is_admin==False)

class UserAdminViews(sqla.ModelView):
    column_list = ['username']
    column_formatters = {'username':format_user_name}
    can_edit = True

    def on_model_change(self, form, model, is_created):
        model.password = generate_password_hash(model.password)

    def get_query(self):
      return self.session.query(self.model).filter(self.model.is_admin==True)

def create_admin(username, password):
    if User.query.filter_by(username=username).first():
        raise RuntimeError(f'{username} ja esta cadastrado')
    admin = User(username=username, password=password, is_admin=True)
    db.session.add(admin)
    db.session.commit()
    return admin

def init_app(app):
    admin.name = app.config.TITLE
    admin.template_mode = "bootstrap3"
    admin.init_app(app)
    admin.add_view(UserAdminViews(User, db.session,name='Admin'))
    admin.add_view(UserView(User, db.session,endpoint='user_admin'))
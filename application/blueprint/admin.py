from flask import Blueprint, request
from flask import render_template, redirect, url_for
from flask_login import login_user, logout_user,current_user
from sqlalchemy.exc import SQLAlchemyError
from application.models import User


admin_blueprint = Blueprint('admin_secury', __name__)

@admin_blueprint.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    errors = None
    username = ''
    if request.method == 'POST':
        
        username = request.form['name']
        password = request.form['password']
        if username and password:
            try:
                user = User.query.filter_by(username=username).first()
                if user and user.is_admin and user.verify_password(password):
                    login_user(user)
                    return redirect(url_for('admin.index'))
                else:
                    errors = 'Usuario invalido'
            except SQLAlchemyError:
                errors = 'Ocorreu um erro desconhecido, tente Novamente!'
        else:
            errors = 'Campos invalidos!'
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin.index'))
    return render_template('admin/login.html', errors=errors, name=username)

@admin_blueprint.route('/admin_logout')
def admin_logout():
    logout_user()
    return redirect(url_for('.admin_login'))

def init_app(app):
    app.register_blueprint(admin_blueprint)
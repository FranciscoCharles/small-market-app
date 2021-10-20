from flask import Blueprint, request
from flask import render_template, redirect, url_for
from flask_login import login_user, logout_user

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
@main_blueprint.route('/home')
def home():
    return render_template('home.html')

@main_blueprint.route('/about')
def about():
    return render_template('about.html')

@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')
    
@main_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('.login'))

def init_app(app):
    app.register_blueprint(main_blueprint)
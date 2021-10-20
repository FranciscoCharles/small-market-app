import click
from flask import current_app
from flask.cli import with_appcontext
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_utils import database_exists, create_database, drop_database
from application.ext.admin import create_admin as my_create_admin
from application.ext.database import db

@click.command()
@with_appcontext
def create_db():
    """Creates database"""
    try:
        database_uri = current_app.config['SQLALCHEMY_DATABASE_URI']
        if not database_exists(database_uri):
            create_database(database_uri)
        db.create_all()
    except SQLAlchemyError as error:
        print('Create DB error:', error)

@click.command()
@with_appcontext
def drop_db():
    """Drop database"""
    try:
        database_uri = current_app.config['SQLALCHEMY_DATABASE_URI']
        if database_exists(database_uri):
            drop_database(database_uri)
    except SQLAlchemyError as error:
        print('Drop DB error:', error)

@click.command()
@click.option('--username', '-u')
@click.option('--password', '-p')
@with_appcontext
def create_admin(username, password):
        """Adds a new user to the database"""
        return my_create_admin(username, password)


def init_app(app):

    for command in [create_db, drop_db]:
        app.cli.add_command(command)
    
    app.cli.add_command(create_admin)
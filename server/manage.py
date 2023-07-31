# services/users/manage.py
import os
import sys

from flask.cli import FlaskGroup
from flask import current_app as app
from models import User, ValidationEntry, db

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

cli = FlaskGroup(app)


@cli.command('create')
def create_db():

    engine = create_engine('mysql+pymysql://bv:test1234@bv.mysql:3306/bv')
    if not database_exists(engine.url):
        create_database(engine.url)

    print(database_exists(engine.url))
    
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('seed')
def seed_db():
    """Seeds the database."""
    db.session.add(User(
        username='tonystark',
        email='avengers@gmail.com',
        password='supersecret'
    ))
    db.session.commit()


if __name__ == '__main__':
    cli()
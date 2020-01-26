import logging
import click
from flask import current_app, g
from flask.cli import with_appcontext

import pymysql
import pandas as pd
import numpy as np

from app.config import config


class MySQL:
    def __init__(self):
        self._conn = pymysql.connect(
            host='localhost',  # mysql server address
            port=3306,  # port num
            user=config['development'].MYSQL_USERNAME,  # username
            passwd=config['development'].MYSQL_PASSWORD,  # password
            charset='utf8',
        )
        self._cur = self._conn.cursor()

    def execute(self, sql):
        self._cur.execute(sql)

    def create(self):
        logging.info("Start to initialize the database...")

        with current_app.open_resource('schema.sql') as f:
            for sql in f.read().decode('utf8').split(';'):
                try:
                    self._cur.execute(sql)
                except Exception as err:
                    if err.args[0] != 1065:
                        logging.error(err)

    def clear(self):
        logging.info("Start to delete and clear the database...")

        try:
            self._cur.execute('DROP DATABASE IF EXISTS `smartedu`;')
        except Exception as err:
            logging.error(err)

    def __del__(self):
        self._conn.close()


def create_db():
    g.db = MySQL()
    g.db.create()


def clear_db():
    g.db = MySQL()
    g.db.clear()


def get_db():
    if 'db' not in g:
        g.db = MySQL()
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        del db


@click.command('create-db')
@with_appcontext
def create_db_command():
    '''Create new tables.'''
    create_db()
    click.echo('Initialized the database.')


@click.command('clear-db')
@with_appcontext
def clear_db_command():
    '''Clear the existing database.'''
    clear_db()
    click.echo('Deleted the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(create_db_command)
    app.cli.add_command(clear_db_command)

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
        with current_app.open_resource('schema.sql') as f:
            for sql in f.read().decode('utf8').split(';'):
                try:
                    self._cur.execute(sql)
                except Exception as err:
                    logging.error(err)

    def execute(self, sql):
        self._cur.execute(sql)

    def __del__(self):
        self._conn.close()


def init_db():
    g.db = MySQL()


@click.command('init-db')
@with_appcontext
def init_db_command():
    '''Clear the existing data and create new tables.'''
    init_db()
    click.echo('Initialized the database.')


def get_db():
    if 'db' not in g:
        g.db = init_db()

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        del db


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def query_db(query, args=(), one=False):
        cur = get_db().execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with current_app.open_resource('SQL/DDL.sql') as f:
        db.executescript(f.read().decode('utf8'))

def sample_data_db():
    db = get_db()
    with current_app.open_resource('SQL/SampleData.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
    sample_data_db()
    click.echo('Filled the database with sample data.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
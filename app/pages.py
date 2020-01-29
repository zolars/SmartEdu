import logging

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for)
from werkzeug.exceptions import abort

# from app.auth import login_required
from app.db import get_db

bp = Blueprint('pages', __name__)


@bp.route('/', methods=('GET', 'POST'))
def index():
    db = get_db()
    if request.method == 'POST':
        keyword = request.form['keyword']
        # Todo
        logging.info("Search for " + keyword)
        return redirect(url_for('pages.index'))

    return render_template('index.html')


@bp.route('/resources')
def resources():
    db = get_db()
    return render_template('index.html')


@bp.route('/video')
def video():
    db = get_db()
    return render_template('index.html')


@bp.route('/book')
def book():
    db = get_db()
    return render_template('index.html')


@bp.route('/exercise')
def exercise():
    db = get_db()
    return render_template('index.html')


@bp.route('/homework')
def homework():
    db = get_db()
    return render_template('index.html')

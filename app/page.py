import json
import logging

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for)
from werkzeug.exceptions import abort

# from app.auth import login_required
from app.utils import *
from app.db import get_db, close_db

bp = Blueprint('page', __name__)


@bp.route('/', methods=('GET', 'POST'))
def index():
    record_page_history('page.index', request.remote_addr)
    if request.method == 'POST':
        keyword = request.form['keyword']
        # Todo
        logging.info("Search for " + keyword)
        return redirect(url_for('page.index'))

    return render_template('page/index.html')


@bp.route('/resources')
def resources():
    return render_template('page/index.html')


@bp.route('/video')
def video():
    return render_template('page/index.html')


@bp.route('/book')
def book():
    return render_template('page/index.html')


@bp.route('/exercise')
def exercise():
    return render_template('page/index.html')


@bp.route('/homework')
def homework():
    return render_template('page/index.html')

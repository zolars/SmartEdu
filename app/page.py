import json
import logging

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for)
from werkzeug.exceptions import abort

from app.utils import *
from app.db import get_db, close_db
from app.auth import login_required

bp = Blueprint('page', __name__)


@bp.route('/', methods=('GET', 'POST'))
def index():
    record_page_history(page_path='/', user_ip=request.remote_addr)
    if request.method == 'POST':
        keyword = request.form['keyword']
        # Todo
        logging.info("Search for " + keyword)
        return redirect(url_for('page.index'))

    return render_template('/page/index.html')


@bp.route('/resources')
def resources():
    record_page_history(page_path='/resources', user_ip=request.remote_addr)
    return render_template('/page/index.html')


@bp.route('/video')
def video():
    record_page_history(page_path='/video', user_ip=request.remote_addr)
    return render_template('/page/index.html')


@bp.route('/book')
def book():
    record_page_history(page_path='/book', user_ip=request.remote_addr)
    return render_template('/page/index.html')


@bp.route('/exercise')
@login_required
def exercise():
    record_page_history(page_path='/exercise', user_ip=request.remote_addr)
    return render_template('/page/index.html')


@bp.route('/homework')
@login_required
def homework():
    record_page_history(page_path='/homework', user_ip=request.remote_addr)
    return render_template('/page/index.html')


@bp.route('/app')
def app():
    record_page_history(page_path='/app', user_ip=request.remote_addr)
    return render_template('/page/index.html')


@bp.route('/exam')
@login_required
def exam():
    record_page_history(page_path='/exam', user_ip=request.remote_addr)
    return render_template('/page/index.html')


@bp.route('/statistics')
@login_required
def statistics():
    record_page_history(page_path='/statistics', user_ip=request.remote_addr)
    return render_template('/page/index.html')

import inspect
import logging

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for)
from werkzeug.exceptions import abort

# from app.auth import login_required
from app.db import get_db, close_db

bp = Blueprint('page', __name__)


# Record page_history
def record_page_history(page_path, user_ip):
    import json

    db = get_db()
    if g.user == '{}' or g.user is None:
        user_id = None
    else:
        user_id = json.loads(g.user)['id']

    if user_id is not None:
        db.execute(
            'INSERT INTO page_history (user_id, user_ip, page_path, time) VALUES ("{user_id}", "{user_ip}", "{page_path}", {time})'
            .format(user_id=user_id,
                    user_ip=user_ip,
                    page_path=page_path,
                    time="now()"))
        db.commit()
    else:
        db.execute(
            'INSERT INTO page_history (user_id, user_ip, page_path, time) VALUES (null, "{user_ip}", "{page_path}", {time})'
            .format(user_ip=user_ip, page_path=page_path, time="now()"))
        db.commit()
    flash('记录页面信息("{user_id}", {user_ip}, "{page_path}", {time})'.format(
        user_id=user_id, user_ip=user_ip, page_path=page_path, time="now()"))

    close_db()


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

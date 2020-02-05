import json
import logging
from datetime import datetime as dt

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for)
from werkzeug.exceptions import abort

from app.utils import record_page_history
from app.files import check_stared
from app.db import get_db, close_db
from app.auth import login_required

bp = Blueprint('page', __name__)


@bp.route('/', methods=('GET', 'POST'))
def index():
    record_page_history(pagepath='/', user_ip=request.remote_addr)
    if request.method == 'POST':
        keyword = request.form['keyword']
        # Todo
        logging.info("Search for " + keyword)
        return redirect(url_for('page.index'))

    return render_template('/page/index.html')


@bp.route('/resources', methods=('GET', 'POST'))
def resources():
    record_page_history(pagepath='/resources', user_ip=request.remote_addr)

    db = get_db()

    chapter_focused = request.args.get("chapter")
    if chapter_focused != 'all' and chapter_focused:
        chapter_focused = int(chapter_focused)
    else:
        chapter_focused = 0

    df = db.fetchall('SELECT * FROM chapter_info')
    df = df.sort_values(by="id", ascending=True)

    chapter_names = ['全部章节'] + df.name.tolist()

    items = []
    for _, row in db.fetchall('SELECT * FROM res_info').iterrows():
        title = row['title']
        if row['type'] == 1:
            filetype = 'video'
        elif row['type'] == 2:
            filetype = 'doc'
        elif row['type'] == 3:
            filetype = 'other'
        filepath = row['context']
        enter_time = str(row['enter_time'])[0:10]
        df = db.fetchall(
            'SELECT username FROM admin_info WHERE id={user_id}'.format(
                user_id=row['enter_user']))
        enter_username = df.iloc[0].username
        chapter_id = row['chapter_id']
        description = row['description']

        if chapter_focused == 0 or chapter_focused == chapter_id:
            items.append({
                'title': title,
                'filetype': filetype,
                'filepath': filepath,
                'enter_time': enter_time,
                'enter_username': enter_username,
                'description': description
            })

    dict = {
        'type': '所有资源',
        'chapter_focused': chapter_focused,
        'chapter_names': chapter_names,
        'items': items,
        'url': 'resources'
    }

    close_db()
    return render_template('/page/resources.html', **dict)


@bp.route('/video')
def video():
    record_page_history(pagepath='/video', user_ip=request.remote_addr)

    db = get_db()

    chapter_focused = request.args.get("chapter")
    if chapter_focused != 'all' and chapter_focused:
        chapter_focused = int(chapter_focused)
    else:
        chapter_focused = 0

    df = db.fetchall('SELECT * FROM chapter_info')
    df = df.sort_values(by="id", ascending=True)

    chapter_names = ['全部章节'] + df.name.tolist()

    items = []
    for _, row in db.fetchall('SELECT * FROM res_info').iterrows():
        title = row['title']
        if row['type'] == 1:
            filetype = 'video'
        else:
            continue

        filepath = row['context']
        enter_time = str(row['enter_time'])[0:10]
        df = db.fetchall(
            'SELECT username FROM admin_info WHERE id={user_id}'.format(
                user_id=row['enter_user']))
        enter_username = df.iloc[0].username
        chapter_id = row['chapter_id']
        description = row['description']

        if chapter_focused == 0 or chapter_focused == chapter_id:
            items.append({
                'title': title,
                'filetype': filetype,
                'filepath': filepath,
                'enter_time': enter_time,
                'enter_username': enter_username,
                'description': description
            })

    dict = {
        'type': '教学视频',
        'chapter_focused': chapter_focused,
        'chapter_names': chapter_names,
        'items': items,
        'url': 'video'
    }

    close_db()
    return render_template('/page/resources.html', **dict)


@bp.route('/doc')
def doc():
    record_page_history(pagepath='/doc', user_ip=request.remote_addr)

    db = get_db()

    chapter_focused = request.args.get("chapter")
    if chapter_focused != 'all' and chapter_focused:
        chapter_focused = int(chapter_focused)
    else:
        chapter_focused = 0

    df = db.fetchall('SELECT * FROM chapter_info')
    df = df.sort_values(by="id", ascending=True)

    chapter_names = ['全部章节'] + df.name.tolist()

    items = []
    for _, row in db.fetchall('SELECT * FROM res_info ORDER BY id').iterrows():
        title = row['title']
        if row['type'] == 2:
            filetype = 'doc'
        else:
            continue

        filepath = row['context']
        enter_time = str(row['enter_time'])[0:10]
        df = db.fetchall(
            'SELECT username FROM admin_info WHERE id={user_id}'.format(
                user_id=row['enter_user']))
        enter_username = df.iloc[0].username
        chapter_id = row['chapter_id']
        description = row['description']

        if chapter_focused == 0 or chapter_focused == chapter_id:
            items.append({
                'title': title,
                'filetype': filetype,
                'filepath': filepath,
                'enter_time': enter_time,
                'enter_username': enter_username,
                'description': description
            })

    dict = {
        'type': '书籍课件',
        'chapter_focused': chapter_focused,
        'chapter_names': chapter_names,
        'items': items,
        'url': 'doc'
    }

    close_db()
    return render_template('/page/resources.html', **dict)


@bp.route('/exercise')
@login_required
def exercise():
    record_page_history(pagepath='/exercise', user_ip=request.remote_addr)
    return render_template('/page/index.html')


@bp.route('/homework')
@login_required
def homework():
    record_page_history(pagepath='/homework', user_ip=request.remote_addr)
    return render_template('/page/index.html')


@bp.route('/app')
def app():
    record_page_history(pagepath='/app', user_ip=request.remote_addr)
    return render_template('/page/index.html')


@bp.route('/exam')
@login_required
def exam():
    record_page_history(pagepath='/exam', user_ip=request.remote_addr)
    return render_template('/page/index.html')


@bp.route('/statistics')
@login_required
def statistics():
    record_page_history(pagepath='/statistics', user_ip=request.remote_addr)
    return render_template('/page/index.html')


@bp.route('/comments')
@login_required
def comments():
    record_page_history(pagepath='/comments', user_ip=request.remote_addr)
    return render_template('/page/index.html')
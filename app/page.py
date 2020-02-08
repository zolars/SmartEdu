import os
import json
import logging
from datetime import datetime as dt

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for)
from werkzeug.exceptions import abort

from app.utils import *
from app.res import check_stared
from app.hw import record_hw_history, check_submitted
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
    chapter_focused, chapter_names = get_chapter_names(chapter_focused)

    items = []
    for _, row in db.fetchall('SELECT * FROM res_info').iterrows():
        title = row['title']
        if row['type'] == 1:
            filetype = 'video'
        elif row['type'] == 2:
            filetype = 'doc'
        elif row['type'] == 3:
            filetype = 'other'

        context = row['context']
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
                'context': context,
                'enter_time': enter_time,
                'enter_username': enter_username,
                'description': description
            })

    dict = {
        'type': 'All',
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
    chapter_focused, chapter_names = get_chapter_names(chapter_focused)

    items = []
    for _, row in db.fetchall('SELECT * FROM res_info').iterrows():
        title = row['title']
        if row['type'] == 1:
            filetype = 'video'
        else:
            continue

        context = row['context']
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
                'context': context,
                'enter_time': enter_time,
                'enter_username': enter_username,
                'description': description
            })

    dict = {
        'type': 'Video',
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
    chapter_focused, chapter_names = get_chapter_names(chapter_focused)

    items = []
    for _, row in db.fetchall('SELECT * FROM res_info ORDER BY id').iterrows():
        title = row['title']
        if row['type'] == 2:
            filetype = 'doc'
        else:
            continue

        context = row['context']
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
                'context': context,
                'enter_time': enter_time,
                'enter_username': enter_username,
                'description': description
            })

    dict = {
        'type': 'Courseware',
        'chapter_focused': chapter_focused,
        'chapter_names': chapter_names,
        'items': items,
        'url': 'doc'
    }

    close_db()
    return render_template('/page/resources.html', **dict)


@bp.route('/exercises')
@login_required
def exercises():
    record_page_history(pagepath='/exercises', user_ip=request.remote_addr)
    db = get_db()

    chapter_focused = request.args.get("chapter")
    chapter_focused, chapter_names = get_chapter_names(chapter_focused)

    items = []
    for _, row in db.fetchall('SELECT * FROM exe_info ORDER BY id').iterrows():
        context = row['context']
        enter_time = str(row['enter_time'])[0:10]
        df = db.fetchall(
            'SELECT username FROM admin_info WHERE id={user_id}'.format(
                user_id=row['enter_user']))
        enter_username = df.iloc[0].username
        chapter_id = row['chapter_id']
        difficulty = row['difficulty']

        if chapter_focused == 0 or chapter_focused == chapter_id:
            items.append({
                'context': context,
                'enter_time': enter_time,
                'enter_username': enter_username,
                'difficulty': difficulty
            })

    dict = {
        'chapter_focused': chapter_focused,
        'chapter_names': chapter_names,
        'items': items,
        'url': 'exercises'
    }

    close_db()
    return render_template('/page/exercises.html', **dict)


@bp.route('/answer', methods=('GET', 'POST'))
@login_required
def answer():
    record_page_history(pagepath='/answer', user_ip=request.remote_addr)
    if request.method == 'POST':
        contexts = request.form['contexts']
        contexts = contexts.replace(" ", "").split(",")

        items = []
        for context in contexts:
            items.append({'context': context})

        dict = {'items': items}
        return render_template('/page/answer.html', **dict)

    else:
        flash("目前无法访问该页面！", "error")
        return redirect(url_for('page.index'))


@bp.route('/homework')
@login_required
def homework():
    record_page_history(pagepath='/homework', user_ip=request.remote_addr)
    db = get_db()

    chapter_focused = request.args.get("chapter")
    chapter_focused, chapter_names = get_chapter_names(chapter_focused)

    items = []
    for _, row in db.fetchall('SELECT * FROM hw_info ORDER BY id').iterrows():
        context = row['context']
        enter_time = str(row['enter_time'])[0:10]
        df = db.fetchall(
            'SELECT username FROM admin_info WHERE id={user_id}'.format(
                user_id=row['enter_user']))
        enter_username = df.iloc[0].username
        chapter_id = row['chapter_id']
        week = row['week']

        if chapter_focused == 0 or chapter_focused == chapter_id:
            items.append({
                'context': context,
                'enter_time': enter_time,
                'enter_username': enter_username,
                'week': week
            })

    dict = {
        'chapter_focused': chapter_focused,
        'chapter_names': chapter_names,
        'items': items,
        'url': 'homework'
    }

    close_db()
    return render_template('/page/homework.html', **dict)


@bp.route('/detail/<context>', methods=('GET', 'POST'))
@login_required
def detail(context):
    record_page_history(pagepath='/detail', user_ip=request.remote_addr)

    db = get_db()
    df = db.fetchall('SELECT * FROM hw_info WHERE context="{context}"'.format(
        context=context))
    row = df.iloc[0]

    enter_time = str(row['enter_time'])[0:10]
    df = db.fetchall(
        'SELECT username FROM admin_info WHERE id={user_id}'.format(
            user_id=row['enter_user']))
    enter_username = df.iloc[0].username
    chapter_id = row['chapter_id']
    week = row['week']

    submitted, time = check_submitted(context)
    if request.method == 'POST' and (not submitted):
        show_ans = True

        if 'file' not in request.files:
            flash('您没有上传文件，请先选择要上传的文件。', 'error')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('您没有上传文件，请先选择要上传的文件。', 'error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            if (g.user != '{}') and (g.user is not None):
                student_id = json.loads(g.user)['student_id']
                try:
                    os.makedirs(
                        os.path.join('files', 'hw', context, str(student_id)))
                    file.save(
                        os.path.join('files', 'hw', context, str(student_id),
                                     file.filename))
                    record_hw_history(request.remote_addr, 1, context)
                except Exception as err:
                    flash("抱歉，操作失败，请联系管理员，错误信息：" + err.message, "error")
                    return redirect(page.index)
        else:
            flash('请检查选择的文件格式！', 'error')
            return redirect(request.url)

        submitted, time = check_submitted(context)
        flash("您已于{}成功提交作业！".format(time.strftime('%Y.%m.%d %H:%M:%S')),
              "success")
    elif submitted:
        show_ans = True
        flash("您已于{}成功提交作业！".format(time.strftime('%Y.%m.%d %H:%M:%S')),
              "success")
    else:
        show_ans = False

    dict = {
        'context': context,
        'enter_time': enter_time,
        'enter_username': enter_username,
        'week': week,
        'url': 'detail',
        'show_ans': show_ans
    }

    close_db()
    return render_template('/page/detail.html', **dict)


@bp.route('/ai_exercises')
@login_required
def ai_exercises():
    record_page_history(pagepath='/ai_exercises', user_ip=request.remote_addr)

    ids = get_prob_ids('ai_exercises')

    items = []
    for id in ids:
        db = get_db()
        df = db.fetchall(
            'SELECT context FROM exe_info WHERE id={id}'.format(id=id))
        context = df.iloc[0].context
        items.append({'context': context})
        close_db()
    dict = {'items': items, 'url': 'exam'}
    return render_template('/page/ai_exercises.html', **dict)


@bp.route('/exam')
@login_required
def exam():
    record_page_history(pagepath='/exam', user_ip=request.remote_addr)

    ids = get_prob_ids('exam')

    items = []
    for id in ids:
        db = get_db()
        df = db.fetchall(
            'SELECT context FROM exe_info WHERE id={id}'.format(id=id))
        context = df.iloc[0].context
        items.append({'context': context})
        close_db()
    dict = {'items': items, 'url': 'exam'}
    return render_template('/page/building.html', **dict)


@bp.route('/statistics')
@login_required
def statistics():
    record_page_history(pagepath='/statistics', user_ip=request.remote_addr)
    return render_template('/page/statistics.html')


@bp.route('/comments')
@login_required
def comments():
    record_page_history(pagepath='/comments', user_ip=request.remote_addr)
    return render_template('/page/building.html')


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

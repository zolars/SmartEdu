import os
import json
import logging
from datetime import datetime as dt

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for)
from werkzeug.exceptions import abort

from app.utils import *
from app.res import check_marked
from app.exe import record_exe_history
from app.hw import record_hw_history, record_sp_exe_history, check_submitted
from app.db import get_db, close_db
from app.auth import login_required

bp = Blueprint('page', __name__)


@bp.route('/', methods=('GET', 'POST'))
def index():
    record_page_history(pagepath='/', user_ip=request.remote_addr)
    with open("./files/index.json", 'r') as index_json:
        index_json = json.load(index_json)
    dict = index_json
    if request.method == 'POST':
        keyword = request.form['keyword']
        return render_template('/page/search.html')
    else:
        return render_template('/page/index.html', **dict)


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
        'type': 'All Course Materials',
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
        ans_A = row['ans_A']
        ans_B = row['ans_B']
        ans_C = row['ans_C']
        ans_D = row['ans_D']

        if chapter_focused == 0 or chapter_focused == chapter_id:
            items.append({
                'context': context,
                'ans_A': ans_A,
                'ans_B': ans_B,
                'ans_C': ans_C,
                'ans_D': ans_D,
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
        abort(404)


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
    expire_time = str(row['expire_time']).replace("-", "/")
    df = db.fetchall(
        'SELECT username FROM admin_info WHERE id={user_id}'.format(
            user_id=row['enter_user']))
    enter_username = df.iloc[0].username
    week = row['week']

    r = int(json.loads(g.user)['student_id']) % 100
    if r == 0:
        r = 100
    r = r * row['r_times']

    ids = row['sp_exe_ids'].split(',')

    items = []
    for id in ids:
        df = db.fetchall(
            'SELECT context, ans_formula FROM sp_exe_info WHERE id={id}'.
            format(id=id))
        sp_context = df.iloc[0].context
        ans_formula = df.iloc[0].ans_formula
        items.append({'context': sp_context, 'ans_formula': ans_formula})

    close_db()

    submitted, time = check_submitted(context, operation=1)
    if request.method == 'POST' and (not submitted):
        show_sp_exe = True
        if 'file' not in request.files:
            flash('您没有上传文件，请先选择要上传的文件。', 'error')
            close_db()
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('您没有上传文件，请先选择要上传的文件。', 'error')
            close_db()
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
                    flash(
                        "Sorry, the file has existed. Please contact the administrator!"
                        + err.message, "error")
                    close_db()
                    return redirect(url_for('page.index'))
        else:
            flash('请检查选择的文件格式！', 'error')
            close_db()
            return redirect(request.url)

        submitted, time = check_submitted(context, operation=1)
        flash(
            "You have submitted the file at {}!".format(
                time.strftime('%Y.%m.%d %H:%M:%S')), "success")
    elif submitted:
        show_sp_exe = True
        flash(
            "You have submitted the file at {}!".format(
                time.strftime('%Y.%m.%d %H:%M:%S')), "success")
    else:
        show_sp_exe = False

    submitted, time = check_submitted(context, operation=2)
    if request.method == 'POST' and (not submitted):
        show_ans = True

        try:
            for item in items:
                record_sp_exe_history(context=item['context'],
                                      user_ip=request.remote_addr,
                                      operation=2,
                                      ans=request.form[item['context']])
        except Exception as err:
            logging.error("error location 1 : ", err)
            close_db()
            return redirect(request.url)

        record_hw_history(request.remote_addr, 2, context)
        submitted, time = check_submitted(context, operation=2)
        flash(
            "You have submitted the Multiple-Choice at {}!".format(
                time.strftime('%Y.%m.%d %H:%M:%S')), "success")
    elif submitted:
        show_ans = True
        flash(
            "You have submitted the Multiple-Choice at {}!".format(
                time.strftime('%Y.%m.%d %H:%M:%S')), "success")
    else:
        show_ans = False

    dict = {
        'context': context,
        'items': items,
        'enter_time': enter_time,
        'expire_time': expire_time,
        'enter_username': enter_username,
        'week': week,
        'r': r,
        'url': 'detail',
        'show_sp_exe': show_sp_exe,
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
        df = db.fetchall('SELECT * FROM exe_info WHERE id={id}'.format(id=id))
        context = df.iloc[0].context
        ans_A = df.iloc[0].ans_A
        ans_B = df.iloc[0].ans_B
        ans_C = df.iloc[0].ans_C
        ans_D = df.iloc[0].ans_D
        items.append({
            'context': context,
            'ans_A': ans_A,
            'ans_B': ans_B,
            'ans_C': ans_C,
            'ans_D': ans_D
        })
        close_db()
    dict = {'items': items, 'url': 'ai_exercises'}
    return render_template('/page/ai_exercises.html', **dict)


@bp.route('/exam', methods=('GET', 'POST'))
@login_required
def exam():
    record_page_history(pagepath='/exam', user_ip=request.remote_addr)

    ids = get_prob_ids('exam')

    items = []
    done = 0
    score = 0
    for id in ids:
        db = get_db()
        df = db.fetchall('SELECT * FROM exe_info WHERE id={id}'.format(id=id))
        context = df.iloc[0].context
        ans_A = df.iloc[0].ans_A
        ans_B = df.iloc[0].ans_B
        ans_C = df.iloc[0].ans_C
        ans_D = df.iloc[0].ans_D
        items.append({
            'context': context,
            'ans_A': ans_A,
            'ans_B': ans_B,
            'ans_C': ans_C,
            'ans_D': ans_D
        })
        close_db()

        if request.method == 'POST':
            done = 1
            ans = request.form[context]
            record_exe_history(context=context,
                               user_ip=request.remote_addr,
                               operation=2,
                               ans=ans)
            df = db.fetchall(
                'SELECT ans FROM exe_info WHERE context="{context}"'.format(
                    context=context))
            if ans == df.ans[0]:
                score += 1

    score = str(score) + " / " + str(len(items))

    dict = {'items': items, 'done': done, 'score': score, 'url': 'exam'}
    return render_template('/page/exam.html', **dict)


@bp.route('/statistics')
@login_required
def statistics():
    record_page_history(pagepath='/statistics', user_ip=request.remote_addr)
    return render_template('/page/statistics.html')


@bp.route('/features')
@login_required
def features():
    record_page_history(pagepath='/features', user_ip=request.remote_addr)
    return render_template('/page/statistics.html')


@bp.route('/comments', methods=('GET', 'POST'))
@login_required
def comments():
    record_page_history(pagepath='/comments', user_ip=request.remote_addr)

    if (g.user != '{}') and (g.user is not None):
        user_id = json.loads(g.user)['id']
        db = get_db()

        if request.method == 'POST':
            comment = request.form['comment']

            db.execute(
                'INSERT INTO cmt_history (user_id, time, comment) VALUES ({user_id}, now(), "{comment}")'
                .format(user_id=user_id, comment=comment))
            db.commit()

            close_db()

            flash('Your comment has been posted!', 'success')
            return 'success'

        else:
            items = []
            for _, row in db.fetchall(
                    'SELECT * FROM cmt_history ORDER BY id').iterrows():
                df = db.fetchall(
                    'SELECT username FROM user_info WHERE id={user_id}'.format(
                        user_id=row['user_id']))
                username = df.iloc[0].username
                comment = row['comment']
                time = row['time']
                items.append({
                    'username': username,
                    'comment': comment,
                    'time': time
                })

            dict = {'items': items}
            return render_template('/page/comments.html', **dict)


def allowed_file(filename):
    allowed_extensions = {'pdf', 'jpg', 'png', 'doc', 'docx'}

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

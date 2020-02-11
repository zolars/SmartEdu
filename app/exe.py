import os
import json
import logging

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for, make_response, send_from_directory)
from werkzeug.exceptions import abort

from app.db import get_db, close_db
from app.auth import login_required

bp = Blueprint('exe', __name__)


@bp.route('/prob_img/<context>', methods=('GET', 'POST'))
def prob_img(context):
    import base64
    img_stream = ''
    with open('./files/exe/' + context + '/prob.png', 'rb') as f:
        img_stream = f.read()
    return img_stream


@bp.route('/ans_img/<context>', methods=('GET', 'POST'))
def ans_img(context):
    import base64
    img_stream = ''
    with open('./files/exe/' + context + '/ans.png', 'rb') as f:
        img_stream = f.read()
    return img_stream


@bp.route('/check_ans', methods=('GET', 'POST'))
def check_ans():
    if request.method == 'POST':
        context = request.form["context"]
        ans = request.form["ans"]
        if (context != "" and ans != ""):
            db = get_db()
            record_exe_history(context=context,
                               user_ip=request.remote_addr,
                               operation=2,
                               ans=ans)
            df = db.fetchall(
                'SELECT ans FROM exe_info WHERE context="{context}"'.format(
                    context=context))
            correct_ans = df.ans[0]
            close_db()

            if ans == correct_ans:
                return 'correct'
            else:
                return 'wrong'
        else:

            return 'unselected'
    else:
        return 'error'


# Record exe_history
def record_exe_history(context,
                       user_ip,
                       operation,
                       ans="null",
                       difficulty="null",
                       answer_easy_if="null"):
    db = get_db()
    if (g.user != '{}') and (g.user is not None):
        user_id = json.loads(g.user)['id']

        df = db.fetchall(
            'SELECT id FROM exe_info WHERE context="{context}"'.format(
                context=context))
        exe_id = df.id[0]
        if operation == 2:
            db.execute(
                'INSERT INTO exe_history (user_id, user_ip, exe_id, operation, time, ans, difficulty, answer_easy_if) VALUES ({user_id}, "{user_ip}", {exe_id}, {operation}, now(), {ans}, {difficulty}, {answer_easy_if})'
                .format(user_id=user_id,
                        user_ip=user_ip,
                        exe_id=exe_id,
                        operation=operation,
                        ans='"' + ans + '"',
                        difficulty=difficulty,
                        answer_easy_if=answer_easy_if))
            db.commit()
        elif operation == 3:
            db.execute(
                'INSERT INTO exe_history (user_id, user_ip, exe_id, operation, time, ans, difficulty, answer_easy_if) VALUES ({user_id}, "{user_ip}", {exe_id}, {operation}, now(), {ans}, {difficulty}, {answer_easy_if})'
                .format(user_id=user_id,
                        user_ip=user_ip,
                        exe_id=exe_id,
                        operation=operation,
                        ans=ans,
                        difficulty=difficulty,
                        answer_easy_if=answer_easy_if))
            db.commit()

    close_db()


@bp.route('/exe_rating/<context>', methods=('GET', 'POST'))
@login_required
def rating(context):
    if request.method == 'POST':
        difficulty = request.form["difficulty"]
        answer_easy_if = request.form["answer_easy_if"]
        if (difficulty != "" and answer_easy_if != ""):
            record_exe_history(context=context,
                               user_ip=request.remote_addr,
                               operation=3,
                               difficulty='"' + difficulty + '"',
                               answer_easy_if='"' + answer_easy_if + '"')
            if check_rating(context) > 0:
                return 'overwrite'
            else:
                return 'success'
        else:
            return 'unselected'
    else:
        return 'error'


# Check rating status with { user_id, exe_id }
def check_rating(context):
    db = get_db()
    if (g.user != '{}') and (g.user is not None):
        user_id = json.loads(g.user)['id']

        df = db.fetchall(
            'SELECT id FROM exe_info WHERE context="{context}"'.format(
                context=context))
        exe_id = df.id[0]

        df = db.fetchall(
            'SELECT user_id FROM exe_history WHERE user_id="{user_id}" AND operation=3 AND exe_id={exe_id}'
            .format(user_id=user_id, exe_id=exe_id))
        amount = len(df)

        close_db()

        return amount - 1

    else:
        close_db()
        return False
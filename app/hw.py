import os
import json
import logging

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for, make_response, send_from_directory)
from werkzeug.exceptions import abort

from app.db import get_db, close_db
from app.auth import login_required

bp = Blueprint('hw', __name__)


@bp.route('/hw_img/<context>', methods=('GET', 'POST'))
def hw_img(context):
    import base64
    img_stream = ''
    with open('./files/hw/' + context + '/prob.png', 'rb') as f:
        img_stream = f.read()
    return img_stream


@bp.route('/sp_prob_img/<context>', methods=('GET', 'POST'))
def sp_prob_img(context):
    import base64
    img_stream = ''
    with open('./files/sp_exe/' + context + '/prob.png', 'rb') as f:
        img_stream = f.read()
    return img_stream


@bp.route('/sp_ans_img/<context>', methods=('GET', 'POST'))
def sp_ans_img(context):
    import base64
    img_stream = ''
    with open('./files/sp_exe/' + context + '/ans.png', 'rb') as f:
        img_stream = f.read()
    return img_stream


# Record hw_history
def record_hw_history(user_ip, operation, context=None):

    if (g.user != '{}') and (g.user is not None):
        user_id = json.loads(g.user)['id']

        if (operation == 1 or operation == 2) and context:
            db = get_db()
            df = db.fetchall(
                'SELECT id FROM hw_info WHERE context="{context}"'.format(
                    context=context))
            hw_id = df.id[0]
            db.execute(
                'INSERT INTO hw_history (user_id, user_ip, hw_id, operation, time) VALUES ({user_id}, "{user_ip}", {hw_id}, {operation}, now())'
                .format(user_id=user_id,
                        user_ip=user_ip,
                        hw_id=hw_id,
                        operation=operation))
            db.commit()

            close_db()


# Record sp_exe_history
def record_sp_exe_history(context,
                          user_ip,
                          operation,
                          ans="null",
                          difficulty="null",
                          answer_easy_if="null"):
    db = get_db()
    if (g.user != '{}') and (g.user is not None):
        user_id = json.loads(g.user)['id']

        df = db.fetchall(
            'SELECT id FROM sp_exe_info WHERE context="{context}"'.format(
                context=context))
        sp_exe_id = df.id[0]
        db.execute(
            'INSERT INTO sp_exe_history (user_id, user_ip, sp_exe_id, operation, time, ans, difficulty, answer_easy_if) VALUES ({user_id}, "{user_ip}", {sp_exe_id}, {operation}, now(), {ans}, {difficulty}, {answer_easy_if})'
            .format(user_id=user_id,
                    user_ip=user_ip,
                    sp_exe_id=sp_exe_id,
                    operation=operation,
                    ans=ans,
                    difficulty=difficulty,
                    answer_easy_if=answer_easy_if))
        db.commit()

    close_db()


# Check submit status with { user_id, hw_id }
def check_submitted(context, operation):
    db = get_db()
    if (g.user != '{}') and (g.user is not None):
        user_id = json.loads(g.user)['id']

        df = db.fetchall(
            'SELECT id FROM hw_info WHERE context="{context}"'.format(
                context=context))
        hw_id = df.id[0]

        df = db.fetchall(
            'SELECT * FROM hw_history WHERE user_id="{user_id}" AND operation={operation} AND hw_id={hw_id}'
            .format(user_id=user_id, operation=operation, hw_id=hw_id))
        amount = len(df)

        close_db()
        if amount >= 1:
            return True, df.iloc[0].time
        elif amount == 0:
            return False, None

    else:
        close_db()
        return False, None

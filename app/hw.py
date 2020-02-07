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


# Record hw_history
def record_hw_history(user_ip, operation, context=None):

    db = get_db()
    if (g.user != '{}') and (g.user is not None):
        user_id = json.loads(g.user)['id']

        if operation == 1 and context:

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


# Check submit status with { user_id, hw_id }
def check_submitted(context):
    db = get_db()
    if (g.user != '{}') and (g.user is not None):
        user_id = json.loads(g.user)['id']

        df = db.fetchall(
            'SELECT id FROM hw_info WHERE context="{context}"'.format(
                context=context))
        hw_id = df.id[0]

        df = db.fetchall(
            'SELECT * FROM hw_history WHERE user_id="{user_id}" AND operation=1 AND hw_id={hw_id}'
            .format(user_id=user_id, hw_id=hw_id))
        amount = len(df)

        close_db()
        if amount >= 1:
            return True, df.iloc[0].time
        elif amount == 0:
            return False, None

    else:
        close_db()
        return False, None

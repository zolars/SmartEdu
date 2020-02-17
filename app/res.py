import os
import json
import logging

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for, make_response, send_from_directory)
from werkzeug.exceptions import abort

from app.db import get_db, close_db
from app.auth import login_required
from app.utils import init_vod_client, get_video_playauth

bp = Blueprint('res', __name__)


@bp.route('/download/<filetype>/<context>', methods=('GET', 'POST'))
@login_required
def download(filetype, context):
    record_res_history(context=context,
                       user_ip=request.remote_addr,
                       operation=2)
    directory = os.getcwd()
    filename = ''
    for temp in os.listdir(directory + '/files/' + filetype + '/' + context):
        if temp != 'cover.png' and temp != '.DS_Store':
            filename = temp

    if filetype == 'video':
        vid = open('./files/' + filetype + '/' + context + '/' + filename,
                   "r").readline()
        try:
            clt = init_vod_client()
            playAuth = get_video_playauth(clt, vid)
            print(playAuth)
        except Exception as e:
            print(e)

        dict = {'vid': vid, 'playAuth': playAuth}
        return render_template('/page/video.html', **dict)
    else:
        response = make_response(
            send_from_directory(directory,
                                './files/' + filetype + '/' + context + '/' +
                                filename,
                                as_attachment=True))
        response.headers["Content-Disposition"] = " filename={}".format(
            filename.encode().decode('latin-1'))  # attachment;

        return response


@bp.route('/cover/<filetype>/<context>', methods=('GET', 'POST'))
def cover(filetype, context):
    import base64
    img_stream = ''
    with open('./files/' + filetype + '/' + context + '/cover.png', 'rb') as f:
        img_stream = f.read()
    return img_stream


@bp.route('/mark/<context>', methods=('GET', 'POST'))
@login_required
def mark(context):
    record_res_history(context=context,
                       user_ip=request.remote_addr,
                       operation=1)
    return check_marked(context)


# Check mark status with { user_id, res_id }
@bp.route('/check_marked/<context>', methods=('GET', 'POST'))
def check_marked(context):
    db = get_db()
    if (g.user != '{}') and (g.user is not None):
        user_id = json.loads(g.user)['id']

        df = db.fetchall(
            'SELECT id FROM res_info WHERE context="{context}"'.format(
                context=context))
        res_id = df.id[0]

        df = db.fetchall(
            'SELECT user_id FROM res_history WHERE user_id="{user_id}" AND operation=1 AND res_id={res_id}'
            .format(user_id=user_id, res_id=res_id))
        amount = len(df)

        close_db()

        if amount % 2 == 1:
            return "marked"
        else:
            return "unmarked"
    else:
        close_db()
        return "unmarked"


@bp.route('/res_rating/<context>', methods=('GET', 'POST'))
@login_required
def rating(context):
    if request.method == 'POST':
        rating = request.form["rating"]
        difficulty = request.form["difficulty"]
        if (rating != "" and difficulty != ""):
            record_res_history(context=context,
                               user_ip=request.remote_addr,
                               operation=3,
                               rating='"' + rating + '"',
                               difficulty='"' + difficulty + '"')
            if check_rating(context) > 0:
                return 'overwrite'
            else:
                return 'success'
        else:
            return 'unselected'
    else:
        return 'error'


# Check rating status with { user_id, res_id }
def check_rating(context):
    db = get_db()
    if (g.user != '{}') and (g.user is not None):
        user_id = json.loads(g.user)['id']

        df = db.fetchall(
            'SELECT id FROM res_info WHERE context="{context}"'.format(
                context=context))
        res_id = df.id[0]

        df = db.fetchall(
            'SELECT user_id FROM res_history WHERE user_id="{user_id}" AND operation=3 AND res_id={res_id}'
            .format(user_id=user_id, res_id=res_id))
        amount = len(df)

        close_db()

        return amount - 1

    else:
        close_db()
        return False


# Record res_history
def record_res_history(context,
                       user_ip,
                       operation,
                       rating="null",
                       difficulty="null"):

    db = get_db()
    if (g.user != '{}') and (g.user is not None):
        user_id = json.loads(g.user)['id']

        df = db.fetchall(
            'SELECT id FROM res_info WHERE context="{context}"'.format(
                context=context))
        res_id = df.id[0]
        db.execute(
            'INSERT INTO res_history (user_id, user_ip, res_id, operation, time, rating, difficulty) VALUES ({user_id}, "{user_ip}", {res_id}, {operation}, now(), {rating}, {difficulty})'
            .format(user_id=user_id,
                    user_ip=user_ip,
                    res_id=res_id,
                    operation=operation,
                    rating=rating,
                    difficulty=difficulty))
        db.commit()

    close_db()

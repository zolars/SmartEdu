import os
import json
import logging
import random
from pyecharts import options as opts
from pyecharts.charts import Pie

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for, make_response, send_from_directory)
from werkzeug.exceptions import abort

from app.db import get_db, close_db
from app.auth import login_required
from app.utils import get_chapter_names

bp = Blueprint('statistics', __name__)


@bp.route("/pieChart")
@login_required
def pieChart() -> Pie:
    db = get_db()
    df = db.fetchall('SELECT * FROM chapter_info')
    df = df.sort_values(by="id", ascending=True)
    chapters = df.name.tolist()

    dict = {}
    for chapter in chapters:
        dict[chapter] = 0

    if (g.user != '{}') and (g.user is not None):
        user_id = json.loads(g.user)['id']

        df = db.fetchall(
            'SELECT res_id FROM res_history WHERE user_id="{user_id}" AND operation=2'
            .format(user_id=user_id))
        for _, row in df.iterrows():
            df = db.fetchall(
                'SELECT chapter_id FROM res_info WHERE id="{res_id}"'.format(
                    res_id=row['res_id']))
            df = db.fetchall(
                'SELECT name FROM chapter_info WHERE id="{chapter_id}"'.format(
                    chapter_id=df.chapter_id[0]))
            chapter_name = df.name[0]
            dict[chapter_name] += 1
    data = []
    for (k, v) in dict.items():
        data.append((k, v))

    c = (Pie().add(
        "", data).set_global_opts(title_opts=opts.TitleOpts()).set_series_opts(
            label_opts=opts.LabelOpts(formatter="{b}: {c}")))

    close_db()
    return c.dump_options_with_quotes()
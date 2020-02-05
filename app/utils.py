import json
import logging

from flask import (flash, g, redirect)

from app.db import get_db, close_db


# Record page_history
def record_page_history(pagepath, user_ip):
    db = get_db()
    if g.user == '{}' or g.user is None:
        user_id = None
    else:
        user_id = json.loads(g.user)['id']

    if user_id is not None:
        db.execute(
            'INSERT INTO page_history (user_id, user_ip, pagepath, time) VALUES ({user_id}, "{user_ip}", "{pagepath}", now())'
            .format(user_id=user_id, user_ip=user_ip, pagepath=pagepath))
        db.commit()
    else:
        db.execute(
            'INSERT INTO page_history (user_id, user_ip, pagepath, time) VALUES (null, "{user_ip}", "{pagepath}", now())'
            .format(user_ip=user_ip, pagepath=pagepath))
        db.commit()

    close_db()


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

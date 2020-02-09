import json
import logging

from flask import (flash, g, redirect)

from app.db import get_db, close_db


def get_chapter_names(chapter_focused):
    db = get_db()

    if chapter_focused != 'all' and chapter_focused:
        chapter_focused = int(chapter_focused)
    else:
        chapter_focused = 0

    df = db.fetchall('SELECT * FROM chapter_info')
    df = df.sort_values(by="id", ascending=True)

    chapter_names = ['全部章节'] + df.name.tolist()

    close_db()

    return chapter_focused, chapter_names


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


def get_prob_ids(type):
    if (g.user != '{}') and (g.user is not None):
        user_id = json.loads(g.user)['id']

        if type == "exam":
            return [1, 3, 5]
        if type == "ai_exercises":
            return [2, 3, 4]

    else:
        return []

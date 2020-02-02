import json

from flask import (flash, g, redirect)

from app.db import get_db, close_db


# Record page_history
def record_page_history(page_path, user_ip):

    db = get_db()
    if g.user == '{}' or g.user is None:
        user_id = None
    else:
        user_id = json.loads(g.user)['id']

    if user_id is not None:
        db.execute(
            'INSERT INTO page_history (user_id, user_ip, page_path, time) VALUES ("{user_id}", "{user_ip}", "{page_path}", {time})'
            .format(user_id=user_id,
                    user_ip=user_ip,
                    page_path=page_path,
                    time="now()"))
        db.commit()
    else:
        db.execute(
            'INSERT INTO page_history (user_id, user_ip, page_path, time) VALUES (null, "{user_ip}", "{page_path}", {time})'
            .format(user_ip=user_ip, page_path=page_path, time="now()"))
        db.commit()
    flash('记录页面信息("{user_id}", {user_ip}, "{page_path}", {time})'.format(
        user_id=user_id, user_ip=user_ip, page_path=page_path, time="now()"))

    close_db()

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

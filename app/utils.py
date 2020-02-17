import json
import logging

from flask import (flash, g, redirect)

from app.db import get_db, close_db

from aliyunsdkcore.client import AcsClient
from aliyunsdkvod.request.v20170321 import GetVideoPlayAuthRequest


def get_chapter_names(chapter_focused):
    db = get_db()

    if chapter_focused != 'all' and chapter_focused:
        chapter_focused = int(chapter_focused)
    else:
        chapter_focused = 0

    df = db.fetchall('SELECT * FROM chapter_info')
    df = df.sort_values(by="id", ascending=True)

    chapter_names = ['All Chapters'] + df.name.tolist()

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


def init_vod_client(accessKeyId='LTAI4FnKKApEWXhNSzKp5ZGV',
                    accessKeySecret='cW5zECBcXOkzcgGIxeooPwFaWs5Uau'):
    regionId = 'cn-beijing'  # 点播服务接入区域
    connectTimeout = 3  # 连接超时，单位为秒
    return AcsClient(accessKeyId,
                     accessKeySecret,
                     regionId,
                     auto_retry=True,
                     max_retry_time=3,
                     timeout=connectTimeout)


def get_video_playauth(clt, videoId):
    request = GetVideoPlayAuthRequest.GetVideoPlayAuthRequest()
    request.set_accept_format('JSON')
    request.set_VideoId(videoId)
    request.set_AuthInfoTimeout(3000)
    response = json.loads(clt.do_action_with_exception(request))
    return response['PlayAuth']

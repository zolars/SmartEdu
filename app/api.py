import json
import logging
from flask import (flash, g)

from werkzeug.exceptions import abort


def get_prob_ids(type):
    if (g.user != '{}') and (g.user is not None):
        user_id = json.loads(g.user)['id']

        if type == "exam":
            return [1, 3, 5]
        if type == "ai_exercises":
            return [2, 4]

    else:
        return []

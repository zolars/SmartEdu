from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for)
from werkzeug.exceptions import abort

# from app.auth import login_required
from app.db import get_db

bp = Blueprint('statistics', __name__)


@bp.route('/statistics')
def statistics():
    db = get_db()
    return render_template('index.html')


@bp.route('/exam')
def exam():
    db = get_db()
    return render_template('index.html')

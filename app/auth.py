import re
import logging
import pandas as pd
import functools

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        student_id = request.form['student_id']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        # role = request.form['role']
        role = 1
        reg_ip = request.remote_addr

        db = get_db()
        error = None

        if not username:
            error = '请填写用户名！'
        elif ' ' in username:
            error = '用户名必须为中英文和数字, 不能包含空格！'
        elif not re.match(r'^\d{10}$', student_id):
            error = '请填写正确的学号！'
        elif not password:
            error = '请填写密码！'
        elif len(password) < 8:
            error = '密码不能少于8位！'
        elif password_confirm != password:
            error = '请确认填写的密码是否相同！'
        elif len(
                db.fetchall(
                    'SELECT id FROM user_info WHERE username = "{username}"'.
                    format(username=username))) > 0:
            error = '用户{username}已存在，请更改用户名。'.format(username=username)
        elif len(
                db.fetchall(
                    'SELECT id FROM user_info WHERE student_id = "{student_id}"'
                    .format(student_id=student_id))) > 0:
            error = '学号{student_id}已注册账号。如有问题，请联系老师或管理员。'.format(
                student_id=student_id)

        logging.info(
            db.fetchall(
                'SELECT id FROM user_info WHERE username = "{username}"'.
                format(username=username)))

        if error is None:
            db.execute(
                'INSERT INTO user_info (username, student_id, password, role, reg_ip, reg_time) VALUES ("{username}", {student_id}, "{password}", {role}, "{reg_ip}", {reg_time})'
                .format(username=username,
                        student_id=student_id,
                        password=generate_password_hash(password),
                        role=role,
                        reg_ip=reg_ip,
                        reg_time="now()"))
            db.commit()
            flash('注册成功。欢迎，{username}！'.format(username=username), 'success')
            return redirect(url_for('auth.register'))

        flash(error, 'error')

    return render_template('auth/login.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute('SELECT * FROM user WHERE username = ?',
                          (username, )).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM user WHERE id = ?',
                                  (user_id, )).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

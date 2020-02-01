import re
import logging
import pandas as pd
import functools

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db, close_db
import app.page

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

            close_db()
            return redirect(url_for('page.index'))

        flash(error, 'error')

    close_db()
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.fetchall(
            'SELECT * FROM user_info WHERE username = "{username}"'.format(
                username=username))

        if len(user) == 0:
            error = '该用户未注册，请先注册！'
        elif not check_password_hash(user['password'][0], password):
            error = '密码错误，请确认填写无误。'

        if error is None:
            session.clear()
            session['user_id'] = int(user['id'][0])
            flash("您已成功登录！", "success")

            close_db()
            return redirect(url_for('page.index'))

        flash(error, "error")

    close_db()
    return render_template('auth/login.html')


@bp.route('/modifyAccount', methods=('GET', 'POST'))
def modifyAccount():
    return render_template('auth/modifyAccount.html')


# 将登录的用户信息存入g
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().fetchall(
            'SELECT * FROM user_info WHERE id = "{user_id}"'.format(
                user_id=user_id)).iloc[0].to_json(orient='index')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/logout')
def logout():
    session.clear()
    flash("您已成功注销！", "success")
    return redirect(url_for('page.index'))

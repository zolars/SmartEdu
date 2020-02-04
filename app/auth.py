import re
import json
import logging
import pandas as pd
import functools

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from app.utils import *
from app.db import get_db, close_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


# 将登录的用户信息存入g
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        try:
            g.user = get_db().fetchall(
                'SELECT * FROM user_info WHERE id = "{user_id}"'.format(
                    user_id=user_id)).iloc[0].to_json(orient='index')
        except Exception as err:
            logging.error(err)
            session.clear()
            g.user = None


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('抱歉，访问此页面请先登录！', 'error')
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/register', methods=('GET', 'POST'))
def register():
    record_page_history(page_path='/auth/register',
                        user_ip=request.remote_addr)
    if request.method == 'POST':
        db = get_db()

        username = request.form['username']
        student_id = request.form['student_id']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        reg_ip = request.remote_addr

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
                'INSERT INTO user_info (username, student_id, password, reg_ip, reg_time)'
                +
                'VALUES ("{username}", {student_id}, "{password}", "{reg_ip}", {reg_time})'
                .format(username=username,
                        student_id=student_id,
                        password=generate_password_hash(password),
                        reg_ip=reg_ip,
                        reg_time='now()'))
            db.commit()
            flash('注册成功。欢迎，{username}！'.format(username=username), 'success')

            close_db()
            return redirect(url_for('page.index'))

        flash(error, 'error')
        close_db()

    return render_template('/auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    record_page_history(page_path='/auth/login', user_ip=request.remote_addr)
    if request.method == 'POST':
        db = get_db()

        username = request.form['username']
        password = request.form['password']
        os = request.form['os']
        browser = request.form['browser']
        resolution = request.form['resolution']

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
            user_id = int(user['id'][0])
            session['user_id'] = user_id

            # Set the id_active as true
            db.execute(
                'UPDATE user_info SET id_active = 1 WHERE id = {user_id}'.
                format(user_id=user_id))

            # Update the table: user_auth_history
            db.execute(
                'INSERT INTO user_auth_history (user_id, user_ip, operation, time, os, browser, resolution)'
                +
                'VALUES ("{user_id}", "{user_ip}", "{operation}", {time}, "{os}", "{browser}", "{resolution}")'
                .format(user_id=user_id,
                        user_ip=request.remote_addr,
                        operation=1,
                        time='now()',
                        os=os,
                        browser=browser,
                        resolution=resolution))
            db.commit()

            flash('您已成功登录！', 'success')

            close_db()
            return redirect(url_for('page.index'))

        flash(error, 'error')
        close_db()

    return render_template('/auth/login.html')


@bp.route('/modifyAccount', methods=('GET', 'POST'))
@login_required
def modifyAccount():
    record_page_history(page_path='/auth/modifyAccount',
                        user_ip=request.remote_addr)
    if request.method == 'POST':
        db = get_db()
        user_id = json.loads(g.user)['id']

        customer_name = request.form['customer_name']
        if customer_name:
            db.execute(
                'UPDATE user_info SET customer_name = "{customer_name}" WHERE id = {user_id}'
                .format(customer_name=customer_name, user_id=user_id))
            db.commit()

        mobile = request.form['mobile']
        if mobile:
            if (not re.match(r'^\d{11}$', mobile)):
                flash('请填写正确的十一位手机号码！', 'error')
            else:
                db.execute(
                    'UPDATE user_info SET mobile = "{mobile}" WHERE id = {user_id}'
                    .format(mobile=mobile, user_id=user_id))
                db.commit()

        birthday = request.form['birthday']
        if birthday:
            db.execute(
                'UPDATE user_info SET birthday = "{birthday}" WHERE id = {user_id}'
                .format(birthday=birthday + ' 00:00:00', user_id=user_id))
            db.commit()

        email = request.form['email']
        if email:
            db.execute(
                'UPDATE user_info SET email = "{email}" WHERE id = {user_id}'.
                format(email=email, user_id=user_id))
            db.commit()

        gender = request.form['gender']
        if gender != '-1':
            db.execute(
                'UPDATE user_info SET gender = {gender} WHERE id = {user_id}'.
                format(gender=gender, user_id=user_id))
            db.commit()
        else:
            db.execute(
                'UPDATE user_info SET gender = {gender} WHERE id = {user_id}'.
                format(gender='null', user_id=user_id))
            db.commit()

        signature = request.form['signature']
        if signature:
            db.execute(
                'UPDATE user_info SET signature = "{signature}" WHERE id = {user_id}'
                .format(signature=signature, user_id=user_id))
            db.commit()

        province = request.form['province']
        if province:
            db.execute(
                'UPDATE user_info SET province = "{province}" WHERE id = {user_id}'
                .format(province=province, user_id=user_id))
            db.commit()

        city = request.form['city']
        if city:
            db.execute(
                'UPDATE user_info SET city = "{city}" WHERE id = {user_id}'.
                format(city=city, user_id=user_id))
            db.commit()

        close_db()
        return redirect(url_for('auth.modifyAccount'))

    return render_template('/auth/modifyAccount.html')


@bp.route('/logout')
@login_required
def logout():
    db = get_db()
    user_id = session['user_id']
    session.clear()
    db.execute(
        'INSERT INTO user_auth_history (user_id, user_ip, operation, time)' +
        'VALUES ("{user_id}", "{user_ip}", "{operation}", {time})'.format(
            user_id=user_id,
            user_ip=request.remote_addr,
            operation=0,
            time='now()'))
    db.commit()
    flash('您已成功注销！', 'success')
    close_db()
    return redirect(url_for('page.index'))

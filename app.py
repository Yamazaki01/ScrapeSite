# -*- encoding:utf-8 -*-
from flask import Flask, redirect, render_template, request, url_for, session

import DBModel
import scrape_re

app = Flask(__name__)

@app.route('/')
def index():
    isUserTable = DBModel.Exists_Tables().exists_create_user()
    if isUserTable:
        msg = 'ログインしてください'
        if 'msg' in session:
            msg = session['msg']
            session.pop('msg')
        return render_template('index.html', msg=msg)
    else:
        return '<p>システムエラー</p>'

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if 'user_name' in session:
        # 全要素削除
        session.clear()
    if request.method == 'POST':
        result_bool = DBModel.Exists_Tables().exists_create_user()
        if result_bool:
            user_name = request.form['user_name']
            user_pass = request.form['user_pass']
            sql_controller_class = DBModel.DB_Controller()
            recode = sql_controller_class.select_user(user_name, user_pass)
            if bool(recode):
                session['user_name'] = recode
                return redirect(url_for('dashbord'))
            else:
                session['msg'] = 'Not User! or Not Password'
        else:
            session['msg'] = 'Not Create DB!'
    return redirect(url_for('index'))

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if 'user_name' in session:
        # 全要素削除
        session.clear()
    return redirect(url_for('index'))

@app.route('/add/user/', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        result_bool = DBModel.Exists_Tables().exists_create_user()
        if result_bool:
            user_name = request.form['user_name']
            user_pass = request.form['user_pass']
            recode = DBModel.DB_Controller().insert_user(user_name, user_pass)
            if bool(recode):
                session['user_name'] = recode
                return redirect(url_for('dashbord'))
            else:
                session['msg'] = "Not Create Account!"
        else:
            session['msg'] = "Not Create DB!"
    return redirect(url_for('index'))

@app.route('/dashbord/')
def dashbord():
    if 'user_name' in session:
        user_name = session['user_name']
    return redirect(url_for('top'))

@app.route('/top/', methods=['GET', 'POST'])
def top():
    if not 'user_name' in session:
        return redirect(url_for('index'))
    else:
        user_name = session['user_name']
    if not 'headers' in session and not 'wait_sec' in session and not 'target_url' in session \
            and not 're_str' in session:
        session['target_url'] = 'http://localhost/'
        headers = 'User-Agent: Mozilla/5.0 (Windows NT 6.1) like Gecko'
        session['headers'] = headers
        session['wait_sec'] = 3
        session['re_str'] = ''
        session['validate_results'] = ''
    headers = session['headers']
    wait_sec = session['wait_sec']
    target_url = session['target_url']
    re_str = session['re_str']
    validate_results = session['validate_results']
    return render_template('top.html', wait_sec=wait_sec, user_name=user_name, \
                           headers=headers, target_url=target_url, re_str=re_str, validate_results=validate_results)
    # return "/top/"

@app.route('/scraping/', methods=['GET', 'POST'])
def scraping():
    session['target_url'] = request.form['target_url']
    session['wait_sec'] = request.form['wait_sec']
    session['headers'] = request.form['headers']
    session['re_str'] = request.form['re_str']
    # session['validate_results'] = ""

    target_url = session['target_url']
    headers = session['headers']
    wait_sec = session['wait_sec']
    re_str = session['re_str']
    validate_results =[]
    validate_results = scrape_re.scraping(target_url, headers, wait_sec, re_str)
    session['validate_results'] = validate_results
    return redirect(url_for('top'))

def main():
    app.secret_key = "!*any secret key*!"
    app.run(debug=True, host='127.0.0.1')

if __name__ == '__main__':
    main()


import sys
import os
import flask
from DataFrame import DataBase
from hashlib import sha256

from flask import Flask  # Подключаем Flask
from flask import render_template  # Подключаем библиотеку для работы с шаблонами
from sqlalchemy import create_engine  # Подключаем библиотеку для работы с базой данных

from flask import request  # Для обработки запросов из форм
from flask import redirect  # Для автоматического перенаправления
import datetime  # Для получения текущей даты и времени
from flask import flash, url_for
from random import randint as rd
from threading import Timer

username = "cshse_40"
passwd = "iliyakonQ1W2"  # lkkjqQ1!
db_name = "cshse_40"

# Раскомментировать после указания базы, логина и пароля

# Создаем приложение
app = Flask(__name__)
db = DataBase(username, passwd, db_name)

authenticated_user = dict()


@app.route("/")
def index():
    if request.remote_addr not in authenticated_user:
        authenticated_user[request.remote_addr] = {'user_id': -1, 'is_authenticated': 0}
    return redirect('/taskboard/0')


@app.route('/taskboard/<int:owner_id>')
def taskboard(owner_id):
    if request.remote_addr not in authenticated_user:
        authenticated_user[request.remote_addr] = {'user_id': -1, 'is_authenticated': 0}
    tasks = db.task_list(owner_id)
    for i, el in enumerate(tasks):
        tasks[i]['position_y'] = rd(0,100)
        tasks[i]['position_x'] = rd(0,100)
    if tasks == 'error':
        return 404
    return render_template('index.html',
                           title='Задания',
                           cur_user=authenticated_user[request.remote_addr],
                           task_list=tasks)


@app.route('/task/<int:task_id>', methods=['POST', 'GET'])
def task(task_id: int):
    if request.remote_addr not in authenticated_user:
        authenticated_user[request.remote_addr] = {'user_id': -1, 'is_authenticated': 0}
    if request.method == 'POST':
        if 'accept_task' in request.form:
            db.user_task_connect(user_id=authenticated_user[request.remote_addr]['user_id'], task_id=task_id)
            Timer(db.get_task(task_id=task_id)['time_to_complete'], db.task_end, kwargs={'user_id' : authenticated_user[request.remote_addr]['user_id'], 'task_id' : task_id}).start()
            return redirect(url_for('taskboard', owner_id = authenticated_user[request.remote_addr]['user_id']))

        if 'drop_task' in request.form:
            db.task_reboot(task_id=task_id)
            db.task_end(task_id=task_id, user_id=authenticated_user[request.remote_addr]['user_id'])
            return redirect(url_for('index'))

    return render_template(
        'task.html', **db.get_task(task_id=task_id),
        cur_user=authenticated_user[request.remote_addr],
        title=f'Задание номер {task_id}'
    )


@app.route('/user/<int:id>')
def user_show(id: int):
    if request.remote_addr not in authenticated_user:
        authenticated_user[request.remote_addr] = {'user_id': -1, 'is_authenticated': 0}
    return f'hello_user_{id}!'


@app.route('/leaderboard')
def leaderboard():
    if request.remote_addr not in authenticated_user:
        authenticated_user[request.remote_addr] = {'user_id': -1, 'is_authenticated': 0}
    return render_template("leaderboard.html",
                           cur_user=authenticated_user[request.remote_addr],
                           users=db.leaderboard(),
                           title='Список лидеров')


@app.route('/item/<int:item_id>')
def item(item_id):
    if request.remote_addr not in authenticated_user:
        authenticated_user[request.remote_addr] = {'user_id': -1, 'is_authenticated': 0}
    return render_template('item.html',
                           **db.get_item(item_id=item_id),
                           cur_user = authenticated_user[request.remote_addr],
                           title = f'Награда {item_id}')

# <------------------------------- Регистрация -------------------------------> #


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.remote_addr not in authenticated_user:
        authenticated_user[request.remote_addr] = {'user_id': -1, 'is_authenticated': 0}
    if request.method == 'POST':
        if not (request.form['lgn'] != '' and request.form['psd'] != ''):
            flash('Нужно заполнить все формы!')
            return redirect('/register')
        else:
            db.user_create(
                login=request.form['lgn'],
                pwd_hash=sha256(request.form['psd'].encode('utf-8')).hexdigest()
                )
            login()
            return redirect(url_for('index'))

    return render_template('login.html',
                           method = 'register',
                           title='Регистрация',
                           cur_user=authenticated_user[request.remote_addr]
                           )


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.remote_addr not in authenticated_user:
        authenticated_user[request.remote_addr] = {'user_id': -1, 'is_authenticated': 0}
    if request.method == 'POST':
        if not (request.form['lgn'] != '' and request.form['psd'] != ''):
            flash('Нужно заполнить все формы!')
            return redirect( url_for(login))
        else:
            user = db.get_user(login=request.form['lgn'], pwd_hash=sha256(request.form['psd'].encode('utf-8')).hexdigest())
            if user == list():
                flash('Введены неверные данные')
                return redirect('/')
            authenticated_user[request.remote_addr] = {
                'name': user['login'],
                'user_id': user['user_id'],
                'is_authenticated': 1
            }

        return redirect(url_for('index'))

    return render_template('login.html',
                           method='login',
                           title='Авторизация',
                           cur_user=authenticated_user[request.remote_addr]
                           )

@app.route('/logout')
def logout():
    authenticated_user[request.remote_addr] = {'user_id': -1, 'is_authenticated': 0}
    return redirect(url_for('index'))

# <------------------------------- Окончание app.route -------------------------------> #


def task_gen():
    Timer(8*60*60, task_gen).start()
    db.task_create()


if __name__ == "__main__":  # Запуск приложения при вызове модуля
    task_gen()
    port = int(os.environ.get("PORT", 6000))
    app.run(host='0.0.0.0', port=port)

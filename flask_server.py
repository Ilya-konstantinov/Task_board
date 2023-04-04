import sys
import os
import flask
from DataFrame import DataBase

from flask import Flask # Подключаем Flask
from flask import render_template # Подключаем библиотеку для работы с шаблонами
from sqlalchemy import create_engine # Подключаем библиотеку для работы с базой данных

from flask import request # Для обработки запросов из форм
from flask import redirect # Для автоматического перенаправления
import datetime # Для получения текущей даты и времени

username = "root"
passwd = "iliyakonQ1W2"  # lkkjqQ1!
db_name = "cshse_40"

# Раскомментировать после указания базы, логина и пароля

# Создаем приложение
app = Flask(__name__)
db = DataBase(username, passwd, db_name)


@app.route("/")
def index():
    return redirect('/taskboard/0')


@app.route('/user/<int:id>')
def user_show(id:int):
    return f'hello_user_{id}!'


@app.route('/leaderboard')
def leaderboard():
    return render_template("leaderboard.html",
                           cur_user = {'id':1, 'is_authenticated': 0},
                           users = db.leaderboard(),
                           title = 'Список лидеров')


@app.route('/user/<int:user_id>/inventory')
def inventory(user_id:int):
    return "hello_inventory"


@app.route('/taskboard/<int:owner_id>')
def taskboard(owner_id):
    tasks = db.task_list(owner_id)
    if (tasks == 'error'):
        return 404
    return render_template('index.html',
                           title = 'Задания',
                           cur_user = {'id':1, 'is_authenticated': 0},
                           task_list = tasks)

if __name__ == "__main__":  # Запуск приложения при вызове модуля
    app.run()
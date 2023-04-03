import sys
import os
import flask
from DataFrame import DataBase

from flask import Flask # Подключаем Flask
from flask import render_template # Подключаем библиотеку для работы с шаблонами
from sqlalchemy import create_engine # Подключаем библиотеку для работы с базой данных

from flask import request # Для обработка запросов из форм
from flask import redirect # Для автоматического перенаправления
import datetime # Для получения текущей даты и врмени

username = "root"
passwd = "iliyakonQ1W2"  # lkkjqQ1!
db_name = "cshse_40"

# Раскомментировать после указания базы, логина и пароля

# Создаем приложение
app = Flask(__name__)
db = DataBase(username, passwd, db_name)


@app.route("/")
def index():
    return 'hello'


@app.route('/user/<int:id>')
def user_show(id:int):
    return f'hello_user_{id}!'


@app.route('/leaderboard')
def leaderboard():
    context = dict()
    return render_template("leaderboard.html",
                           cur_user = {'id':1, 'is_authenticated': 0},
                           users = db.leaderboard(),
                           title = 'Список лидеров')


@app.route('/user/<string:login>/inventory')
def inventory(login:str):
    return "hello_inventory"


@app.route('/taskboard')
def taskboard():
    return "hello_taskboard"

if __name__ == "__main__":  # Запуск приложения при вызове модуля
    app.run()
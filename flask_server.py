import sys
import os
import flask
from DataFrame import DataBase

from flask import Flask  # Подключаем Flask
from flask import render_template  # Подключаем библиотеку для работы с шаблонами
from sqlalchemy import create_engine  # Подключаем библиотеку для работы с базой данных

from flask import request  # Для обработка запросов из форм
from flask import redirect  # Для автоматического перенаправления
import datetime  # Для получения текущей даты и врмени

username = ""
passwd = ""  # lkkjqQ1!
db_name = ""

# Раскомментировать после указания базы, логина и пароля

# Создаем приложение
app = Flask(__name__)

if __name__ == "__main__":  # Запуск приложения при вызове модуля
    app.run()


@app.route('/')
def main():
    pass


@app.route('/user/<int:id>')
def user_show(id:int):
    pass


@app.route('/leaderboard')
def leaderboard():
    pass

@app.route('/user/<string:login>/inventory')
def inventory(login:str):
    pass

@app.route('/taskboard')
def taskboard():
    pass

from mysql.connector import connect
from sqlalchemy import create_engine, text
from random import randint as rd

class DataBase:
    def __init__(self, username:str, passwd:str,  db_name:str):
        self.engine = connect(host='localhost', passwd=passwd, username=username,  database = db_name)

    def db_connect(func_to_decr):
        def connect(self,*args, **kwargs):
            conn = self.engine.cursor()
            # trans = conn.begin()
            ans = func_to_decr(self, conn, *args, **kwargs)
            # trans.commit()
            conn.close()
            return ans
        return connect

    @db_connect
    def user_create(self, cur, login: str, pwd_hash: str, score:int = 0) -> None:
        cur.execute(text(f"INSERT INTO users(login, pwd_hash, score) VALUES(\"{login}\",\"{pwd_hash}\", {score})"))

    @db_connect
    def user_delete(self, cur, user_id: int) -> None:
        cur.execute("DELETE FROM users WHERE user_id = %s", user_id)

    @db_connect
    def user_update(self, cur) -> None:
        pass

    @db_connect
    def add_item(self, cur, user_id:int, item_id:int) -> None:
        cur.execute("UPDATE items SET owner_id = %s WHERE item_id = %s", user_id, item_id)

    @db_connect
    def task_create(self, cur, task_id : int = None) -> None:
        if (task_id is None):
            task_id = rd(0, 4)
        base_task = ("SELECT * FROM tasks_base WHERE task_id = %s", task_id)
        base_task = dict(base_task)
        base_task['difficulty_level'] = rd(0, 4)
        base_task['reward_id'] = rd(0, 4)
        base_task['reward_title'] = cur.execute('SELECT title FROM items WHERE item_id = %s', base_task['reward_id'])

        cur.execute("INSERT INTO tasks("
                              "user_id, task_title, task_description, difficulty_level, picture_path,"
                              "time_to_complete, reward_id, reward_name) "
                              "VALUES("
                              "0, %s, %s, %s, %s, %s, %s, %s"
                              ")", base_task['title'], base_task['description_path'], base_task['difficulty_level'],
                              base_task['picture_path'], base_task['time_to_complete']*base_task['difficulty_level'],
                              base_task['reward_id'], base_task['reward_title'])

    # user_id, task_title, task_description, difficulty_level, picture_path, time_to_complete, reward_id, reward_name

    @db_connect
    def task_end(self, cur, task_id) -> None:
        cur.execute = ("DELETE FROM tasks WHERE task_id = %s", task_id)

    @db_connect
    def task_available(self, cur) -> list[int]:
        tasks_aval_table = cur.execute(text("SELECT FROM tasks WHERE task_id = 0"))
        tasks = [dict(row) for row in tasks_aval_table]
        return tasks

    @db_connect
    def task_not_available(self, cur) -> list[int]:
        tasks_aval_table = cur.execute(text("SELECT FROM tasks WHERE task_id <> 0"))
        tasks = [dict(row) for row in tasks_aval_table]
        return tasks


    @db_connect
    def leaderboard(self, cur) :
        cur.execute("SELECT * FROM users ORDER BY score;")
        ans = list()
        for i, row in enumerate(cur):
            ans.append(dict())
            ans[i]['num'] = i+1
            for name, field in zip(cur.column_names, row):
                ans[i][name] = field
        return ans

    def get_all_users(self):  # Получить список информации о всех пользователях
        cur = self.engine.connect()  # Подключаемся к базе
        all_users_table = cur.execute("select * from user")  # Выполняем запрос и получаем таблицу с результатов
        cur.close()  # Закрываем подключение к базе
        all_users = [dict(row) for row in all_users_table]  # Создаем список строк из таблицы
        return all_users

if __name__ == "__main__":
    db = DataBase(username = "root", passwd = "iliyakonQ1W2", db_name = "cshse_40")
    s = """
    1.user_create(self, cur, login: str, pwd_hash: str )
    2.user_delete(self, cur, user_id: int)
    3.user_update(self, cur)
    4.add_item(self, cur, user_id:int, item_id:int)
    5.task_create(self, cur, task_id : int = None)
    6.task_end(self, cur, task_id)
    7.task_available(self, cur)
    8.task_not_available(self, cur)
    9.leaderboard(self, cur)
    10. get_all_users(self, cur)
    11. Выход
    """
    c = input(s).split()
    while(c[0] != '11'):
        match c[0]:
            case '1':
                db.user_create(login=c[1], pwd_hash=c[2])
            case '2':
                db.user_delete(user_id=int(c[1]))
            case '3':
                pass
            case '4':
                db.add_item(user_id=int(c[1]), item_id=int(c[2]))
            case '5':
                db.task_create()
            case '6':
                db.task_end(task_id=int(c[1]))
            case '7':
                print(db.task_available())
            case '8':
                print(db.task_not_available())
            case '9':
                print(db.leaderboard())
            case '10':
                print(db.get_all_users())
        c = input(s).split()
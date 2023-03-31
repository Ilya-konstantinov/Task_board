from sqlalchemy import create_engine
from random import randint as rd

class DataBase:
    def __init__(self, username:str, passwd:str,  db_name:str):
        self.engine = create_engine("mysql://" + username + ":" + passwd + "@localhost/" + db_name + "?charset=utf8",
                               pool_size=10,
                               max_overflow=20, echo=True)

    def db_connect(func_to_decr):
        def connect(self,*args, **kwargs):
            conn = self.engine.connect()
            trans = conn.begin()
            func_to_decr(self, conn, *args, **kwargs)
            trans.commit()
            conn.close()
        return connect

    @db_connect
    def user_create(self, connection, login: str, pwd_hash: str ) -> None:
        connection.execute("INSERT INTO users(login, pwd_hash) VALUES(%s, %s)", login, pwd_hash)

    @db_connect
    def user_delete(self, connection, user_id: int) -> None:
        connection.execute("DELETE FROM users WHERE user_id = %s", user_id)

    @db_connect
    def user_update(self, connection) -> None:
        pass

    @db_connect
    def add_item(self, connection, user_id:int, item_id:int) -> None:
        connection.execute("UPDATE items SET owner_id = %s WHERE item_id = %s", user_id, item_id)

    @db_connect
    def task_create(self, connection, task_id : int = None) -> None:
        if (task_id is None):
            task_id = rd(0, 4)
        base_task = ("SELECT * FROM tasks_base WHERE task_id = %s", task_id)
        base_task = dict(base_task)
        base_task['difficulty_level'] = rd(0, 4)
        base_task['reward_id'] = rd(0, 4)
        base_task['reward_title'] = connection.execute('SELECT title FROM items WHERE item_id = %s', base_task['reward_id'])

        connection.execute("INSERT INTO tasks("
                              "user_id, task_title, task_description, difficulty_level, picture_path,"
                              "time_to_complete, reward_id, reward_name) "
                              "VALUES("
                              "0, %s, %s, %s, %s, %s, %s, %s"
                              ")", base_task['title'], base_task['description_path'], base_task['difficulty_level'],
                              base_task['picture_path'], base_task['time_to_complete']*base_task['difficulty_level'],
                              base_task['reward_id'], base_task['reward_title'])

    # user_id, task_title, task_description, difficulty_level, picture_path, time_to_complete, reward_id, reward_name

    @db_connect
    def task_end(self, connection, task_id) -> None:
        connection.execute = ("DELETE FROM tasks WHERE task_id = %s", task_id)

    @db_connect
    def task_available(self, connection) -> list[int]:
        tasks_aval_table = connection.execute = ("SELECT FROM tasks WHERE task_id = 0")
        tasks = [dict(row) for row in tasks_aval_table]
        return tasks

    @db_connect
    def task_not_available(self, connection) -> list[int]:
        tasks_aval_table = connection.execute = ("SELECT FROM tasks WHERE task_id <> 0")
        tasks = [dict(row) for row in tasks_aval_table]
        return tasks


    @db_connect
    def leaderboard(self, connection) -> list[tuple]:
        board = connection.execute("SELECT login, score FROM users GROUP BY score ")
        leaderboard = [dict(row) for row in board]
        return leaderboard

if __name__ == "__main__":
    db = DataBase(username = "cshse_40", passwd = "lkkjqQ1!", db_name = "cshse_40")
    s = """
    1.user_create(self, connection, login: str, pwd_hash: str )
    2.user_delete(self, connection, user_id: int)
    3.user_update(self, connection)
    4.add_item(self, connection, user_id:int, item_id:int)
    5.task_create(self, connection, task_id : int = None)
    6.task_end(self, connection, task_id)
    7.task_available(self, connection)
    8.task_not_available(self, connection)
    9.leaderboard(self, connection)
    10. Выход
    """
    c = input(s).split()
    while(c[0] != 10):
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
        c = input().split()
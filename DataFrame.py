from mysql.connector import connect
from sqlalchemy import create_engine, text
from random import randint as rd


def fetchall(cur):
    ans = []
    for i, row in enumerate(cur):
        ans.append(dict())
        ans[-1]['num'] = i
        for name, field in zip(cur.column_names, row):
            ans[i][name] = field
    return ans


def fetchone(cur):
    for row in cur:
        for field in row:
            return field


def origin_task_size(cur):
    return len(fetchall(cur.execute("SELECT * FROM task_base")))


def rewards_size(cur) -> int:
    return len(fetchall(cur.execute("SELECT * FROM item_base")))


class DataBase:
    def __init__(self, username: str, passwd: str, db_name: str):
        self.engine = connect(host='localhost', passwd=passwd, username=username, database=db_name)

    def db_connect(func_to_decr):
        def connect(self, *args, **kwargs):
            conn = self.engine.cursor()
            # trans = conn.begin()
            ans = func_to_decr(self, conn, *args, **kwargs)
            # trans.commit()
            conn.close()
            return ans

        return connect

    @db_connect
    def user_create(self, cur, login: str, pwd_hash: str, score: int = 0, pic_path:str = '') -> None:
        cur.execute(text(f"INSERT INTO users(login, pwd_hash, score, pic_path) VALUES(\"{login}\",\"{pwd_hash}\", {score}, \'{pic_path}\')"))

    @db_connect
    def user_delete(self, cur, user_id: int) -> None:
        cur.execute("DELETE FROM users WHERE user_id = %s", user_id)

    @db_connect
    def user_update(self, cur) -> None:
        pass

    @db_connect
    def add_score(self, cur, user_id: int, score: int) -> None:
        post_score = cur.execute("SELECT score FROM users WHERE user_id = %s", score)
        post_score = [row for row in post_score][0]
        cur.execute("UPDATE users SET score = %s WHERE user_id = %s", post_score + score, user_id)

    @db_connect
    def user_task_connect(self, cur, user_id: int, task_id: int):
        cur.execute('UPDATE tasks SET owner_id = %s WHERE task_id = %s', user_id, task_id)

    @db_connect
    def task_create(self, cur, origin_id: int = None) -> None:
        if (origin_id is None):
            origin_id = rd(0, origin_task_size(cur))
        base_task = fetchall(cur.execute("SELECT * FROM tasks_base WHERE task_id = %s", origin_id))
        base_task['difficulty_level'] = rd(1, 5)
        base_task['reward_id'] = rd(1, rewards_size(cur))
        base_task['reward_title'] = cur.execute('SELECT title FROM items WHERE item_id = %s', base_task['reward_id'])

        cur.execute("INSERT INTO tasks("
                    "user_id, task_title, task_description, difficulty_level,"
                    "reward_id, reward_name, origin_id) "
                    "VALUES("
                    "0, %s, %s, %s, %s, %s, %s"
                    ")", base_task['title'], base_task['description_path'], base_task['difficulty_level'],
                    base_task['reward_id'], base_task['reward_title'], origin_id)

    # user_id, task_title, task_description, difficulty_level, picture_path, time_to_complete, reward_id, reward_name

    @db_connect
    def task_end(self, cur, user_id, task_id) -> None:
        cur.execute('SELECT reward_id FROM tasks WHERE task_id = %s', task_id)
        reward_id = fetchone(cur)
        cur.execute('SELECT score FROM items WHERE item_id = %s', reward_id)
        score_add = fetchone(cur)
        self.add_score(cur=cur, user_id=user_id, score=score_add)
        cur.execute("DELETE FROM tasks WHERE task_id = %s", task_id)

    @db_connect
    def task_list(self, cur, owner_id):
        if not str(owner_id).isdigit():
            return 'error'

        cur.execute(text(
            f"SELECT task_id, reward_id, task_description, origin_id, difficulty_level, reward_name FROM tasks WHERE user_id == {owner_id} "))
        ans = fetchall(cur)
        for i in range(len(ans)):
            cur.execute(text(f'SELECT time_to_complite from tasks_base WHERE task_id == {ans[i]["origin_id"]}'))
            ans[i]['time_to_complite'] = fetchone(cur)

        return ans

    @db_connect
    def leaderboard(self, cur):
        cur.execute("SELECT * FROM users ORDER BY score;")
        return fetchall(cur)

    @db_connect
    def get_user(self, cur, login: str, pwd_hash: str):
        cur.execute(f'SELECT * FROM users WHERE login = {login} and pwd_hash = {pwd_hash}')
        if (len(cur) != 1):
            return []
        else:
            return {title: val for title, val in zip(cur.colomn_names, cur[0])}


if __name__ == "__main__":
    db = DataBase(username="root", passwd="iliyakonQ1W2", db_name="cshse_40")
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
    while (c[0] != '11'):
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

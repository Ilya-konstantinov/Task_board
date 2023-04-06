from mysql.connector import connect
import os
from random import randint as rd


def fetchall(cur):
    ans = []
    if cur is None:
        return []
    for i, row in enumerate(cur):
        ans.append(dict())
        ans[-1]['num'] = i
        for name, field in zip(cur.column_names, row):
            ans[i][name] = field
    return ans


def fetchone(cur):
    if cur is None:
        return None
    for row in cur:
        for field in row:
            return field


def origin_task_size(cur) -> int:
    cur.execute("SELECT * FROM tasks_base;")
    return len(fetchall(cur))


def rewards_size(cur) -> int:
    cur.execute("SELECT * FROM items_base;")
    return len(fetchall(cur))


class DataBase:
    def __init__(self, username: str, passwd: str, db_name: str):
        self.cnx = connect(host='localhost', passwd=passwd, username=username, database=db_name)

    def db_connect(func_to_decr):
        def connect(self, *args, **kwargs):
            conn = self.cnx.cursor()
            ans = func_to_decr(self, conn, *args, **kwargs)
            self.cnx.commit()
            conn.close()
            return ans

        return connect

    @db_connect
    def user_create(self, cur, login: str, pwd_hash: str, score: int = 0, pic_path: str = '') -> None:
        cur.execute(
            f"INSERT INTO users(login, pwd_hash, score, pic_path) VALUES(\"{login}\", \"{pwd_hash}\", {score}, \"{pic_path}\")")

    @db_connect
    def add_score(self, cur, user_id: int, score: int) -> None:
        cur.execute(f"SELECT score FROM users WHERE user_id = {user_id}")
        post_score = fetchone(cur)
        cur.execute(f"UPDATE users SET score = {post_score + score} WHERE user_id = {user_id}")

    @db_connect
    def user_task_connect(self, cur, user_id: int, task_id: int):
        cur.execute(f'UPDATE tasks SET user_id = {user_id} WHERE task_id = {task_id}')

    @db_connect
    def task_create(self, cur, origin_id: int = None) -> None:
        if (origin_id is None):
            origin_id = rd(1, origin_task_size(cur))
        cur.execute(f"SELECT * FROM tasks_base WHERE task_id = {origin_id}")
        base_task = fetchall(cur)[0]
        base_task['difficulty_level'] = rd(1, 5)
        base_task['reward_id'] = self.reward_create(dif_level=base_task['difficulty_level'])
        cur.execute(f'SELECT item_name FROM items WHERE item_id = {base_task["reward_id"]}')
        base_task['reward_title'] = fetchone(cur)
        path = os.path.dirname(os.path.abspath(__file__)) + f'\\static\\discriptions\\{origin_id}.txt'
        with open(path, encoding='utf-8') as f:
            base_task['description'] = f.read()[:30]

        cur.execute("INSERT INTO tasks("
                    "user_id, task_title, task_description, difficulty_level,"
                    "reward_id, reward_name, time_to_complete, origin_id) "
                    "VALUES("
                    f"0, \"{base_task['title']}\", \"{base_task['description']}\", {base_task['difficulty_level']}, "
                    f"{base_task['reward_id']}, \"{base_task['reward_title']}\", {base_task['time_to_complete'] * base_task['difficulty_level']}, {origin_id}"
                    ")")
    @db_connect
    def reward_create(self, cur, dif_level: int = None, origin_id: int = None):
        if origin_id is None:
            origin_id = rd(1, rewards_size(cur))
        if dif_level is None:
            difficulty_level = rd(1, 5)

        cur.execute(f"SELECT * FROM items_base WHERE item_id = {origin_id}")
        base_item = fetchall(cur)[0]
        cur.execute(f"INSERT INTO items(item_name, owner_id, item_description, score) VALUES(\"{base_item['item_name']}\", 0, \"{base_item['item_description']}\", {base_item['score'] * dif_level})")
        cur.execute('SELECT item_id FROM items')
        ans = fetchall(cur)[-1]['item_id']
        return ans

    @db_connect
    def task_end(self, cur, user_id, task_id) -> None:
        cur.execute(f'SELECT reward_id FROM tasks WHERE task_id = {task_id}')
        if len(fetchall(cur)) != 1:
            return
        cur.execute(f'SELECT reward_id FROM tasks WHERE task_id = {task_id}')
        reward_id = fetchone(cur)
        cur.execute(f'SELECT score FROM items WHERE item_id = {reward_id}')
        score_add = fetchone(cur)
        self.add_score(user_id=user_id, score=score_add)
        cur.execute(f"DELETE FROM tasks WHERE task_id = {task_id}")

    @db_connect
    def task_list(self, cur, owner_id):
        if not str(owner_id).isdigit():
            return 'error'

        cur.execute(
            f"SELECT * FROM tasks WHERE user_id={owner_id};"
        )
        ans = fetchall(cur)
        for i in range(len(ans)):
            cur.execute(f'SELECT time_to_complete from tasks_base WHERE task_id = {ans[i]["origin_id"]};')
            ans[i]['time_to_complite'] = fetchone(cur)

        return ans

    @db_connect
    def leaderboard(self, cur, limit: int = 50):
        cur.execute(f"SELECT * FROM users ORDER BY score DESC LIMIT {limit} OFFSET 1;")
        return fetchall(cur)

    @db_connect
    def get_user(self, cur, login: str, pwd_hash: str):
        cur.execute(f'SELECT * FROM users WHERE login = \"{login}\" and pwd_hash = \"{pwd_hash}\";')
        ans = fetchall(cur)
        if len(ans) != 1:
            return []
        else:
            return ans[0]

    @db_connect
    def get_task(self, cur, task_id):
        cur.execute(f"SELECT * FROM tasks WHERE task_id = {task_id};")
        ans = fetchall(cur)[0]
        path = os.path.dirname(os.path.abspath(__file__)) + f"\\static\\discriptions\\{ans['origin_id']}.txt"
        with open(path, encoding='utf-8') as f:
            ans['task_description'] = f.read()

        return ans

    @db_connect
    def get_item(self, cur, item_id):
        cur.execute(f"SELECT * FROM items WHERE item_id = {item_id};")
        return fetchall(cur)[0]

    @db_connect
    def task_reboot(self, cur, task_id):
        cur.execute(f"DELETE FROM tasks WHERE task_id = {task_id};")

    @db_connect
    def user_drop(self, cur, user_id):
        cur.execute(f'DELETE FROM users WHERE user_id = {user_id};')

if __name__ == "__main__":
    db = DataBase(username="root", passwd="iliyakonQ1W2", db_name="cshse_40_2")
    s = """
    1. user_create login: str pwd_hash: str score: int = 0 pic_path: str = ''
    2. add_score user_id: int score: int 
    3. user_task_connect user_id: int task_id: int
    4. task_create origin_id: int = None
    5. reward_create difficulty_level:int = None origin_id:int = None
    6. task_end user_id task_id
    7. task_list owner_id
    8. leaderboard limit:int = 50
    9. get_user login: str, pwd_hash: str
    10. get_task cur task_id
    11. task_reboot task_id
    12. get_item item_id
    13. user_drop user_id
    0. Выход
    """
    c = input(s).split()
    while c[0] != '0':
        match c[0]:
            case '1':
                db.user_create(c[1], c[2])
            case '2':
                db.add_score(int(c[1]), int(c[2]))
            case '3':
                db.user_task_connect(int(c[1]), int(c[2]))
            case '4':
                db.task_create()
            case '5':
                print(db.reward_create())
            case '6':
                db.task_end(int(c[1]), int(c[2]))
            case '7':
                print(db.task_list(owner_id=int(c[1])))
            case '8':
                print(*db.leaderboard())
            case '9':
                print(db.get_user(c[1], c[2]))
            case '10':
                print(db.get_task(int(c[1])))
            case '11':
                print(db.task_reboot(int(c[1])))
            case '12':
                print(db.get_item(item_id=int(c[1])))
        c = input(s).split()

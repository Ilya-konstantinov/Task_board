from sqlalchemy import create_engine

class DataBase:
    def __init__(self, username:str, passwd:str,  db_name:str):
        self.engine = create_engine("mysql://" + username + ":" + passwd + "@localhost/" + db_name + "?charset=utf8",
                               pool_size=10,
                               max_overflow=20, echo=True)

    def db_connect(func_to_decr):
        def connect(self,*args, **kwargs):
            conn = self.engine.connect()
            func_to_decr(self, conn, *args, **kwargs)
            conn.close()
        return connect

    @db_connect
    def user_create(self, connection, login: str, psw_hash: str ) -> None:
        pass

    @db_connect
    def user_delete(self, connection, user_id: int) -> None:
        pass

    @db_connect
    def user_update(self, connection) -> None:
        pass

    @db_connect
    def add_item(self, connection, user_id:int, item_id:int) -> None:
        pass

    @db_connect
    def task_create(self, connection) -> None:
        pass

    @db_connect
    def task_end(self, connection) -> None:
        pass

    @db_connect
    def task_available(self, connection) -> list[int]:
        pass

    @db_connect
    def task_not_available(self, connection) -> list[int]:
        pass

    @db_connect
    def leaderboard(self, connection) -> list[tuple]:
        pass


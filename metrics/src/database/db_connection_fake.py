from src.database.db_connection import DBConnection

class DBConnectionFake(DBConnection):

    def write_event_to_db(self, payload: dict):
        print(f"\nWriting event to db: {payload}\n")
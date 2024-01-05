from src.database.db_connection import DBConnection

class DBConnectionFake(DBConnection):

    def __init__(self, database_name: str = None, table_name: str = None):
        self.database_name = database_name
        self.table_name = table_name

    def write_event_to_db(self, payload: dict):
        print(f"\nWriting event to db: {payload}\n")


    def get_all_repo_events(self, repo_name: str) -> list:
        print(f"\nGetting all repo events for repo: {repo_name}\n")
        return []

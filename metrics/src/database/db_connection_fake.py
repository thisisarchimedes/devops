from src.database.db_connection import DBConnection

class DBConnectionFake(DBConnection):

    FAKE_DB_FILE_PATH = 'test/fake_db/'

    def __init__(self, database_name: str = None, table_name: str = None):
        self.database_name = database_name
        self.table_name = table_name
        self.fake_db_file = f'{self.FAKE_DB_FILE_PATH}{self.database_name}_{self.table_name}.log'
        self.db_read_only = False

    def write_event_to_db(self, payload: dict):
        
        if self.db_read_only:
            return
        
        with open(self.fake_db_file, 'w+') as f:
            f.write(str(payload))

    def get_all_repo_events(self, repo_name: str) -> list:
        with open(self.fake_db_file, 'r') as f:
            return f.readlines()
        
    def set_db_read_only_flag(self, flag: bool) -> None:
        self.db_read_only = flag

from typing import List
import pandas as pd

from src.database.db_connection import DBConnection

class DBConnectionFake(DBConnection):

    FAKE_DB_FILE_PATH = 'test/fake_db/'

    def __init__(self, database_name: str = None, table_name: str = None):
        self.database_name = database_name
        self.table_name = table_name
        self.fake_db_file = f'{self.FAKE_DB_FILE_PATH}{self.database_name}_{self.table_name}.log'
        self.db_read_only = False

    def write_event_to_db(self, event_df: pd.DataFrame) -> None:
        
        if self.db_read_only:
            return

        if event_df.empty:
            raise ValueError("The provided DataFrame is empty.")

        with open(self.fake_db_file, 'w+') as f:
            event_df.to_csv(f, index=False)

    def get_all_repo_events(self, repo_name: str) -> pd.DataFrame:

        df = pd.read_csv(self.fake_db_file)
                
        return df


    def get_daily_deploy_volume(self, repos_name: List[str] = None) -> pd.DataFrame:
        
        df = pd.read_csv(self.fake_db_file)
        return df
        

    def set_db_read_only_flag(self, flag: bool) -> None:
        self.db_read_only = flag

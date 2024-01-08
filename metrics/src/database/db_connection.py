from typing import List
import pandas as pd

class DBConnection():

    def __init__(self, database_name: str, table_name: str):
        self.database_name = database_name
        self.table_name = table_name

    def write_event_to_db(self, event_df: pd.DataFrame) -> None:
        pass

    """
    |Timestamp|Repo|Event|Metadata|
    """
    def get_all_repo_events(self, repo_name: str) -> pd.DataFrame:
        pass

    """
    |Day|DeployCount|
    """
    def get_daily_deploy_volume(self, repos_name: List[str] = None) -> pd.DataFrame:
        pass


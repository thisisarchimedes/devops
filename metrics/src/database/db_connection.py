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
    |Timestamp|Week of <date>|Number of days with at least one deploy|
    """
    def get_days_per_week_with_deploy(self, repos_name: List[str]) -> pd.DataFrame:
        pass


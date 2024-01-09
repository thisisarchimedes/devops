from datetime import datetime, timedelta
from typing import List
import pandas as pd


class DBConnection():

    def __init__(self, database_name: str, table_name: str):
        self.database_name = database_name
        self.table_name = table_name

    def write_event_to_db(self, event_df: pd.DataFrame) -> None:
        pass

    def get_all_events(self) -> pd.DataFrame:
        """
        |Timestamp|Repo|Event|Metadata|
        """
        pass

    def get_repo_events(self, repo_name: str) -> pd.DataFrame:
        """
        |Timestamp|Repo|Event|Metadata|
        """
        pass

    def get_daily_deploy_volume(self, repos_name: List[str] = None) -> pd.DataFrame:
        """
        |Day|DeployCount|
        """
        pass

    def get_deploy_frequency_events_since_date(self, start_date: datetime.date) -> pd.DataFrame:
        pass

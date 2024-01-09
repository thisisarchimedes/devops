from typing import List
import pandas as pd
from datetime import datetime, timedelta

from src.database.db_connection import DBConnection


class DBConnectionFake(DBConnection):

    FAKE_DB_FILE_PATH = 'test/fake_db/db.csv'

    def __init__(self, database_name: str = None, table_name: str = None):
        pass
        

    def write_event_to_db(self, event_df: pd.DataFrame) -> None:
        if event_df.empty:
            raise ValueError("The provided DataFrame is empty.")

        # Format the datetime column to string
        event_df['Time'] = event_df['Time'].dt.strftime('%Y-%m-%d %H:%M:%S.000')

        with open(self.FAKE_DB_FILE_PATH, 'a') as f:
            event_df.to_csv(f, index=False, header=False)

        
    def get_all_events(self) -> pd.DataFrame:
        
        df = pd.read_csv(self.FAKE_DB_FILE_PATH)
        return df


    def get_repo_events(self, repo_name: str) -> pd.DataFrame:

        df = pd.read_csv(self.FAKE_DB_FILE_PATH)
        filtered_df = df[df['Repo'] == repo_name]

        return filtered_df
    

    def get_daily_deploy_volume(self, repos_name: List[str] = None) -> pd.DataFrame:

        df = pd.read_csv(self.FAKE_DB_FILE_PATH)
        df['Time'] = pd.to_datetime(df['Time'])

        # Filter for 'deploy' events
        df = df[df['Event'] == 'deploy']

        # Filter for events in the last 3 months
        three_months_ago = datetime.now() - timedelta(days=90)
        df = df[df['Time'] >= three_months_ago]

        # If a list of repos is provided, filter by those repos
        if repos_name is not None:
            df = df[df['Repo'].isin(repos_name)]

        # Group by day and count
        df['Day'] = df['Time'].dt.date
        deploy_volume = df.groupby('Day').size().reset_index(name='DeployCount')

        return deploy_volume
    

    def get_deploy_frequency_events_since_date(self, start_date: datetime.date) -> pd.DataFrame:

        df = pd.read_csv(self.FAKE_DB_FILE_PATH)
        filtered_df = df[df['Event'] == 'calc_deploy_frequency']

        return filtered_df

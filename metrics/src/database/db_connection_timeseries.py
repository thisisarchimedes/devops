import os
from typing import List
from datetime import datetime, timedelta

import boto3
import awswrangler as wr

import pandas as pd

from src.database.db_connection import DBConnection
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


class DBConnectionTimeseries(DBConnection):

    def __init__(self, database_name: str, table_name: str):
        self.database_name = database_name
        self.table_name = table_name
        self.session = boto3.Session()

    def write_event_to_db(self, event_df: pd.DataFrame) -> None:

        utc_time = datetime.now(timezone.utc)
        event_df['time'] = utc_time

        rejected_records = wr.timestream.write(
            df=event_df,
            database=self.database_name,
            table=self.table_name,
            time_col='time',
            measure_col='metadata',
            dimensions_cols=['repo_name', 'event']
        )

        if len(rejected_records) > 0:
            raise ValueError(
                f"Error writing to Timestream: {rejected_records} records were rejected.")
    
    def get_all_events(self) -> pd.DataFrame:
        query = self.get_query_for_all_events()
        query_result = self.execute_query(query)

        return query_result

    def get_repo_events(self, repo_name: str) -> pd.DataFrame:
        query = self.get_query_for_repo_events(repo_name)
        query_result = self.execute_query(query)

        return query_result

    def get_daily_deploy_volume(self, repos_name: List[str] = None) -> pd.DataFrame:
        query = self.get_daily_deploy_volume_query(repos_name)
        query_result = self.execute_query(query)

        return query_result

    def get_deploy_frequency_events_since_date(self, start_date: datetime.date) -> pd.DataFrame:
        query = self.get_query_for_deploy_frequency_events_since_date(
            start_date)
        query_result = self.execute_query(query)

        return query_result

    def execute_query(self, query: str) -> pd.DataFrame:
        session = boto3.Session()
        return wr.timestream.query(query, boto3_session=session)
    
    def get_query_for_all_events(self) -> str:

        return f"""
                    SELECT 
                        time AS Timestamp, 
                        repo_name AS Repo, 
                        event AS Event, 
                        measure_value::varchar AS Metadata 
                    FROM "{self.database_name}"."{self.table_name}"
                    ORDER BY time ASC
                """

    def get_daily_deploy_volume_query(self, repos: List[str] = None) -> str:
        query = ""
        if (repos is None):
            query = f"""
                SELECT date_trunc('day', time) AS Day, COUNT(*) AS DeployCount
                FROM "{self.database_name}"."{self.table_name}"
                WHERE "event" = 'deploy'
                AND time >= date_add('month', -3, current_date)
                GROUP BY date_trunc('day', time)
            """
        else:
            repo_names_str = self.format_repo_names(repos)
            query = f"""
                SELECT date_trunc('day', time) AS Day, COUNT(*) AS DeployCount
                FROM "{self.database_name}"."{self.table_name}"
                WHERE "event" = 'deploy' AND "repo_name" IN ({repo_names_str})
                AND time >= date_add('month', -3, current_date)
                GROUP BY date_trunc('day', time)
            """

        return query

    def format_repo_names(self, repos: List[str]) -> str:
        return ', '.join(f"'{repo}'" for repo in repos)

    def get_query_for_repo_events(self, repo_name: str) -> str:

        return f"""
                    SELECT 
                        time AS Timestamp, 
                        repo_name AS Repo, 
                        event AS Event, 
                        measure_value::varchar AS Metadata 
                    FROM "{self.database_name}"."{self.table_name}"
                    WHERE "repo_name" = '{repo_name}'
                    ORDER BY time ASC
                """

    def get_query_for_deploy_frequency_events_since_date(self, start_date: datetime.date) -> str:

        return f"""
            SELECT 
                time AS Timestamp, 
                repo_name AS Repo, 
                event AS Event, 
                measure_value::varchar AS Metadata 
            FROM "{self.database_name}"."{self.table_name}"
            WHERE "event" = 'calc_deploy_frequency'
            AND time >= '{start_date}'
            ORDER BY time ASC
        """

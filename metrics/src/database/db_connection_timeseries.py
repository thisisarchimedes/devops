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
            raise ValueError(f"Error writing to Timestream: {rejected_records} records were rejected.")
        
    
    def get_all_repo_events(self, repo_name: str) -> pd.DataFrame:
        query = self.get_query_for_all_repo_events(repo_name)
        query_result = self.execute_query(query)

        return query_result
        

    def get_days_per_week_with_deploy(self, repos: List[str]) -> pd.DataFrame:
        query = self.build_deploy_query(repos)
        query_result = self.execute_query(query)

        return self.process_deploy_data(query_result)
        
    
    def execute_query(self, query: str) -> pd.DataFrame:
        session = boto3.Session()
        return wr.timestream.query(query, boto3_session=session)

    def build_deploy_query(self, repos: List[str]) -> str:
        repo_names_str = self.format_repo_names(repos)
        return f"""
            WITH DailyDeployCount AS (
                SELECT date_trunc('day', time) AS day, COUNT(*) AS deploy_count
                FROM "{self.database_name}"."{self.table_name}"
                WHERE "event" = 'deploy' AND "repo_name" IN ({repo_names_str})
                AND time >= date_add('month', -3, current_date)
                GROUP BY date_trunc('day', time)
            ),
            DaysWithDeployPerWeek AS (
                SELECT date_trunc('week', day) AS week, COUNT(*) AS days_with_deploy
                FROM DailyDeployCount WHERE deploy_count > 0
                GROUP BY date_trunc('week', day)
            )
            SELECT week, days_with_deploy FROM DaysWithDeployPerWeek ORDER BY week ASC
            """

    def format_repo_names(self, repos: List[str]) -> str:
        return ', '.join(f"'{repo}'" for repo in repos)

    
    def process_deploy_data(self, query_response):
        deploy_data = self.parse_query_response(query_response)
        return self.fill_missing_weeks(deploy_data)

    def fill_missing_weeks(self, deploy_data: pd.DataFrame) -> pd.DataFrame:
        deploy_data['week'] = self.normalize_weeks(deploy_data['week'])
        all_weeks = self.generate_week_series()
        return self.merge_week_series_with_data(all_weeks, deploy_data)

    def normalize_weeks(self, week_series: pd.Series) -> pd.Series:
        return pd.to_datetime(week_series).dt.to_period('W-MON').dt.start_time

    def generate_week_series(self) -> pd.DataFrame:
        start_date = datetime.now() - timedelta(weeks=12)
        end_date = datetime.now()
        return pd.date_range(start=start_date, end=end_date, freq='W-MON').to_frame(index=False, name='week')

    def merge_week_series_with_data(self, week_series: pd.DataFrame, data: pd.DataFrame) -> pd.DataFrame:
        merged_data = week_series.merge(data, on='week', how='left')
        merged_data['days_with_deploy'].fillna(0, inplace=True)
        return merged_data
    

    def parse_query_response(self, response) -> pd.DataFrame:
        data = [{'week': row['Data'][0]['ScalarValue'], 
                'days_with_deploy': int(row['Data'][1]['ScalarValue'])}
                for row in response['Rows']]
        return pd.DataFrame(data)


    def prepare_record(self, repo_name, event, metadata) -> dict:

        utc_time = datetime.now(timezone.utc)
        est_time = utc_time.astimezone(ZoneInfo("America/New_York"))

        current_time_milliseconds = int(est_time.timestamp() * 1000)

        return {
            'Dimensions': [
                {'Name': 'repo_name', 'Value': repo_name},
                {'Name': 'event', 'Value': event}
            ],
            'MeasureName': 'event_metadata',
            'MeasureValue': metadata if metadata else 'N/A',
            'MeasureValueType': 'VARCHAR',
            'Time': str(current_time_milliseconds),
            'TimeUnit': 'MILLISECONDS'
        }


    def insert_record_into_timestream(self, client, record):

        try:
            response = client.write_records(DatabaseName=self.database_name, TableName=self.table_name, Records=[record])
            print("Record inserted successfully")
        except client.exceptions.RejectedRecordsException as e:
            print("Some records were rejected.")
            if 'RejectedRecords' in e.response:
                for rejected_record in e.response['RejectedRecords']:
                    print("Rejected Record:", rejected_record)
            else:
                print("Error: RejectedRecords details not found in response.")
        except Exception as e:
            print(f"Error inserting record: {e}")


    def get_query_for_all_repo_events(self, repo_name: str) -> str:
        
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

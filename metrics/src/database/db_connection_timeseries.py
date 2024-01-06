import os
import boto3
from typing import List
import pandas as pd
from datetime import datetime, timedelta

from src.database.db_connection import DBConnection
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

class DBConnectionTimeseries(DBConnection):

    def __init__(self, database_name: str, table_name: str):
        self.database_name = database_name
        self.table_name = table_name

    def write_event_to_db(self, payload: dict):

        client = self.create_timestream_client('timestream-write')
        record = self.prepare_record(payload['repo_name'], payload['event'], payload['metadata'])
        self.insert_record_into_timestream(client, record)
        
    
    def get_all_repo_events(self, repo_name: str) -> list:
        client = self.create_timestream_client('timestream-query')
        query = self.construct_query_for_repo_events(repo_name)

        try:
            response = client.query(QueryString=query)
            return self.parse_repo_events_response(response)
        except Exception as e:
            print(f"Error querying database: {e}")
            return []

    def get_days_per_week_with_deploy(self, repos_name: List[str]) -> pd.DataFrame:
        client = self.create_timestream_client('timestream-query')

        # Convert the list of repository names to a format suitable for the SQL query
        repo_names_str = ', '.join(f"'{name}'" for name in repos_name)

        # Modify the query to include the list of repository names
        query = f"""
        WITH DailyDeployCount AS (
            SELECT date_trunc('day', time) AS day, COUNT(*) AS deploy_count
            FROM "{self.database_name}"."{self.table_name}"
            WHERE "event" = 'deploy'
                AND "repo_name" IN ({repo_names_str})
                AND time >= date_add('month', -3, current_date)
            GROUP BY date_trunc('day', time)
        ),
        DaysWithDeployPerWeek AS (
            SELECT date_trunc('week', day) AS week, COUNT(*) AS days_with_deploy
            FROM DailyDeployCount
            WHERE deploy_count > 0
            GROUP BY date_trunc('week', day)
        )
        SELECT week, days_with_deploy
        FROM DaysWithDeployPerWeek
        ORDER BY week ASC
        """

        try:
            response = client.query(QueryString=query)
            query_results_df = self.parse_days_per_week_response(response)
            print(query_results_df)
            res =  self.fill_missing_weeks(query_results_df)
            print(res)
            return res
        except Exception as e:
            print(f"Error querying database: {e}")
            return pd.DataFrame()

    def fill_missing_weeks(self, query_result_df: pd.DataFrame) -> pd.DataFrame:
        # Normalize week column to the start of the week (e.g., Monday at 00:00:00)
        query_result_df['week'] = pd.to_datetime(query_result_df['week']).dt.to_period('W-MON').dt.start_time

        # Generate a list of all weeks in the last 3 months
        end_date = datetime.now()
        start_date = end_date - timedelta(weeks=12)
        all_weeks = pd.date_range(start=start_date, end=end_date, freq='W-MON').to_frame(index=False, name='week')

        # Normalize all_weeks to the start of the week
        all_weeks['week'] = all_weeks['week'].dt.to_period('W-MON').dt.start_time

        # Merge with query results to find missing weeks
        final_results = all_weeks.merge(query_result_df, on='week', how='left')
        final_results['days_with_deploy'].fillna(0, inplace=True)

        return final_results

    

    def parse_days_per_week_response(self, response) -> pd.DataFrame:
        # Extract data into a DataFrame
        data = []
        for row in response['Rows']:
            week = row['Data'][0]['ScalarValue']
            days_with_deploy = int(row['Data'][1]['ScalarValue'])
            data.append({'week': week, 'days_with_deploy': days_with_deploy})

        return pd.DataFrame(data)

    
    def create_timestream_client(self, client_type: str):
        return boto3.client(client_type)
    

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


    def construct_query_for_repo_events(self, repo_name: str) -> str:
        return f"""
            SELECT * FROM "{self.database_name}"."{self.table_name}"
            WHERE "repo_name" = '{repo_name}'
        """


    def parse_repo_events_response(self, response) -> list:
        events = []
        for row in response['Rows']:
            event = {'Data': row['Data']}
            events.append(event)
        return events



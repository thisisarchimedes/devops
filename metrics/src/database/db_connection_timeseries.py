import os
import boto3
from src.database.db_connection import DBConnection
from datetime import datetime, timezone
import pytz

DATABASE_NAME = 'DORAStats'
TABLE_NAME = 'DORARawEvents'

class DBConnectionTimeseries(DBConnection):

    def write_event_to_db(self, payload: dict):

        client = self.create_timestream_client('timestream-write')
        record = self.prepare_record(payload['repo_name'], payload['event'], payload['metadata'])
        self.insert_record_into_timestream(client, record)
        

    
    def get_all_repo_events(self, repo_name: str) -> list:
        client = boto3.client('timestream-query')

        query = f"""
            SELECT * FROM "{DATABASE_NAME}"."{TABLE_NAME}"
            WHERE "repo_name" = '{repo_name}'
        """

        try:
            response = client.query(QueryString=query)
            events = []

            for row in response['Rows']:
                event = { 'Data': row['Data'] }
                events.append(event)

            return events

        except Exception as e:
            print(f"Error querying database: {e}")
            return []


    def create_timestream_client(self, client_type: str):
        return boto3.client(client_type)


    def prepare_record(self, repo_name, event, metadata) -> dict:

        utc_time = datetime.now(timezone.utc)
        est = pytz.timezone('America/New_York')
        est_time = utc_time.astimezone(est)

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
            response = client.write_records(DatabaseName=DATABASE_NAME, TableName=TABLE_NAME, Records=[record])
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




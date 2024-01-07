from datetime import datetime
import uuid

import pytest
import pandas as pd

from src.database.db_connection_timeseries import DBConnectionTimeseries

class TestDBConnectionTimeseries:

    DATABASE_NAME = 'DORAStats'
    TABLE_NAME = 'DORARawEventsTest'

    def test_write_timeseries(self):

        db_connection = DBConnectionTimeseries(self.DATABASE_NAME, self.TABLE_NAME)

        random_uuid = str(uuid.uuid4())

        events_df = pd.DataFrame([{
            "time": [datetime.now()] ,
            "repo_name": random_uuid,
            "event": 'deploy',
            "metadata": 'test_metadata'
        }])


        try:
            db_connection.write_event_to_db(events_df)
        except Exception as e:
            pytest.fail(f"Error writing to database: {e}")

        res = db_connection.get_all_repo_events(random_uuid)
        assert len(res) == 1, "write_event_to_db() should write one event to the database."


    def test_get_all_repo_events_response_format(self):

        db_connection = DBConnectionTimeseries(self.DATABASE_NAME, self.TABLE_NAME)

        result_df = db_connection.get_all_repo_events("test_repo")

        assert isinstance(result_df, pd.DataFrame), "Result should be a pandas DataFrame"

        expected_columns = ['Timestamp', 'Repo', 'Event', 'Metadata']
        assert all(column in result_df.columns for column in expected_columns), "DataFrame should have all the expected columns"

        assert pd.api.types.is_datetime64_any_dtype(result_df['Timestamp']), "'Timestamp' column should be of datetime type"




    def test_get_deployment_frequency(self):

        return
    
        db_connection = DBConnectionTimeseries(self.DATABASE_NAME, self.TABLE_NAME)

        repos = ["test_repo1", "test_repo2", "test_repo3"]

        res = db_connection.get_days_per_week_with_deploy(repos)
        assert len(res) > 0, "get_deployment_frequency() should return a list of at least one item."

        print (res)

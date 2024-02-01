from datetime import datetime, timedelta
import uuid
import json
import pytest
import pandas as pd

from src.event_processor.database.db_connection_timeseries import DBConnectionTimeseries


class TestDBConnectionTimeseries:

    DATABASE_NAME = 'DORAStats'
    TABLE_NAME = 'DORARawEventsTest'

    def test_write_timeseries(self):

        db_connection = DBConnectionTimeseries(
            self.DATABASE_NAME, self.TABLE_NAME)

        random_uuid = str(uuid.uuid4())

        events_df = pd.DataFrame([{
            "Time": datetime.now(),
            "Repo": random_uuid,
            "Event": 'deploy',
            "Metadata": 'test_metadata'
        }])

        try:
            db_connection.write_event_to_db(events_df)
        except Exception as e:
            pytest.fail(f"Error writing to database: {e}")

        res = db_connection.get_repo_events(random_uuid)
        assert len(res) == 1, "write_event_to_db() should write one event to the database."

    def test_get_all_events_response_format(self):

        db_connection = DBConnectionTimeseries(
            self.DATABASE_NAME, self.TABLE_NAME)

        result_df = db_connection.get_all_events()

        assert isinstance(
            result_df, pd.DataFrame), "Result should be a pandas DataFrame"

        expected_columns = ['Time', 'Repo', 'Event', 'Metadata']
        assert all(
            column in result_df.columns for column in expected_columns), "DataFrame should have all the expected columns"

        assert pd.api.types.is_datetime64_any_dtype(
            result_df['Time']), "'Time' column should be of datetime type"
        
    def test_get_all_repo_events_response_format(self):

        db_connection = DBConnectionTimeseries(
            self.DATABASE_NAME, self.TABLE_NAME)

        result_df = db_connection.get_repo_events("test_repo")

        assert isinstance(
            result_df, pd.DataFrame), "Result should be a pandas DataFrame"

        expected_columns = ['Time', 'Repo', 'Event', 'Metadata']
        assert all(
            column in result_df.columns for column in expected_columns), "DataFrame should have all the expected columns"

        assert pd.api.types.is_datetime64_any_dtype(
            result_df['Time']), "'Time' column should be of datetime type"

    def test_get_daily_deploy_volume(self):

        db_connection = DBConnectionTimeseries(
            self.DATABASE_NAME, self.TABLE_NAME)

        result_df = db_connection.get_daily_deploy_volume(None)

        assert isinstance(
            result_df, pd.DataFrame), "Result should be a pandas DataFrame"

        expected_columns = ['Day', 'DeployCount']
        assert all(
            column in result_df.columns for column in expected_columns), "DataFrame should have all the expected columns"

        assert pd.api.types.is_datetime64_any_dtype(
            result_df['Day']), "'Day' column should be of datetime type"

    def test_get_deploy_frequency_events_since_date(self):

        db_connection = DBConnectionTimeseries(
            self.DATABASE_NAME, self.TABLE_NAME)
        db_connection.write_event_to_db(pd.DataFrame([{
            "Time": datetime.now(),
            "Repo": 'test_repo',
            "Event": 'calc_deploy_frequency',
            "Metadata": 'test_metadata'
        }]))

        start_date = datetime.now() - timedelta(days=90)
        result_df = db_connection.get_deploy_frequency_events_since_date(
            start_date)

        assert isinstance(
            result_df, pd.DataFrame), "Result should be a pandas DataFrame"

        expected_columns = ['Time', 'Repo', 'Event', 'Metadata']
        assert all(
            column in result_df.columns for column in expected_columns), "DataFrame should have all the expected columns"

        assert pd.api.types.is_datetime64_any_dtype(
            result_df['Time']), "'Time' column should be of datetime type"

        assert all(
            result_df['Event'] == 'calc_deploy_frequency'), "Event type should be 'calc_deploy_frequency'"
        
    def test_get_repo_push_event_that_matches_commit_id(self):

        db_connection = DBConnectionTimeseries(
            self.DATABASE_NAME, self.TABLE_NAME)
        
        repo_name = 'test_repo1'

        event_metadata = '{"pass": "true", "commit_id": "caa3fdd16ce75c2fb361905e2767602d95f6d33b" ,"report_url": "https://github.com/thisisarchimedes/OffchainLeverageLedgerBuilder/actions/runs/7743500877"}'
        events_df = pd.DataFrame([{
            "Time": datetime.now(),
            "Repo": repo_name,
            "Event": 'push',
            "Metadata": event_metadata
        }])

        db_connection.write_event_to_db(events_df)

        result_df = db_connection.get_repo_events_by_commit_id(repo_name, "caa3fdd16ce75c2fb361905e2767602d95f6d33b")

        assert isinstance(
            result_df, pd.DataFrame), "Result should be a pandas DataFrame"

        expected_columns = ['Time', 'Repo', 'Event', 'Metadata']
        assert all(
            column in result_df.columns for column in expected_columns), "DataFrame should have all the expected columns"

        assert result_df['Metadata'].iloc[0] == event_metadata, "Metadata should match the event metadata"

    def test_commit_id_in_push_jsonify_able(self):

        db_connection = DBConnectionTimeseries(
            self.DATABASE_NAME, self.TABLE_NAME)
        
        repo_name = 'test_repo1'

        event_metadata = '{"pass": "true", "commit_id": "caa3fdd16ce75c2fb361905e2767602d95f6d33b" ,"report_url": "https://github.com/thisisarchimedes/OffchainLeverageLedgerBuilder/actions/runs/7743500877"}'
        events_df = pd.DataFrame([{
            "Time": datetime.now(),
            "Repo": repo_name,
            "Event": 'push',
            "Metadata": event_metadata
        }])

        db_connection.write_event_to_db(events_df)

        result_df = db_connection.get_repo_events_by_commit_id(repo_name, "caa3fdd16ce75c2fb361905e2767602d95f6d33b")
    
        metadata = json.loads(result_df['Metadata'].iloc[0])
        assert metadata['commit_id'] == "caa3fdd16ce75c2fb361905e2767602d95f6d33b", "Metadata should be jsonified"
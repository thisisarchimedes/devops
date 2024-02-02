import uuid

import pytest
import pandas as pd

from src.event_processor.database.db_connection_fake import DBConnectionFake


class TestDBConnectionFake:

    DATABASE_NAME = 'test/fake_db/'
    TABLE_NAME = 'db.csv'

    def test_get_all_events(self):

        db_connection = DBConnectionFake(
            self.DATABASE_NAME, self.TABLE_NAME)

        df = db_connection.get_all_events()
        num_rows = len(df.index)

        assert num_rows > 0, "get_all_events() should return a non-empty DataFrame"

    def test_write_event_to_db(self):

        db_connection = DBConnectionFake(
            self.DATABASE_NAME, self.TABLE_NAME)

        events_df = pd.DataFrame([{
            "Time": pd.Timestamp.now(),
            "Repo": "test_repo",
            "Event": 'deploy',
            "Metadata": 'test_metadata'
        }])

        df = db_connection.get_all_events()
        num_rows_before = len(df.index)

        db_connection.write_event_to_db(events_df)

        df = db_connection.get_all_events()
        num_rows_after = len(df.index)

        assert num_rows_after == num_rows_before + \
            1, "write_event_to_db() should add a row to the database"

    def test_get_all_repo_events_response_format(self):
        db_connection = DBConnectionFake(
            self.DATABASE_NAME, self.TABLE_NAME)

        df = db_connection.get_repo_events("test_repo2")
        num_rows = len(df.index)

        assert num_rows == 2, "get_repo_events() should return a DataFrame with 2 rows"

    def test_get_daily_deploy_volume(self):
        db_connection = DBConnectionFake(
            self.DATABASE_NAME, self.TABLE_NAME)

        result_df = db_connection.get_daily_deploy_volume(None)

        expected_columns = ['Day', 'DeployCount']
        assert all(
            column in result_df.columns for column in expected_columns), "DataFrame should have all the expected columns"

        assert len(
            result_df.index) > 0, "get_daily_deploy_volume() should return a non-empty DataFrame"

    def test_get_deploy_frequency_events_since_date(self):

        db_connection = DBConnectionFake(
            self.DATABASE_NAME, self.TABLE_NAME)

        db_connection.write_event_to_db(pd.DataFrame([{
            "Time": pd.Timestamp.now(),
            "Repo": 'test_repo',
            "Event": 'calc_deploy_frequency',
            "Metadata": "{'deploy_frequency': 1}"
        }]))

        start_date = pd.Timestamp.now() - pd.Timedelta(days=90)
        result_df = db_connection.get_deploy_frequency_events_since_date(
            start_date)

        assert isinstance(
            result_df, pd.DataFrame), "Result should be a pandas DataFrame"

        expected_columns = ['Time', 'Repo', 'Event', 'Metadata']
        assert all(
            column in result_df.columns for column in expected_columns), "DataFrame should have all the expected columns"

        assert all(
            result_df['Event'] == 'calc_deploy_frequency'), "Event type should be 'calc_deploy_frequency'"

    def test_get_repo_push_event_that_matches_commit_id(self):

        db_connection = DBConnectionFake(
            self.DATABASE_NAME, self.TABLE_NAME)

        repo_name = 'test_repo1'

        event_metadata = '{"pass": "true", "commit_id": "caa3fdd16ce75c2fb361905e2767602d95f6d33b" ,"report_url": "https://github.com/thisisarchimedes/OffchainLeverageLedgerBuilder/actions/runs/7743500877"}'
        events_df = pd.DataFrame([{
            "Time": pd.Timestamp.now(),
            "Repo": repo_name,
            "Event": 'push',
            "Metadata": event_metadata
        }])

        db_connection.write_event_to_db(events_df)

        result_df = db_connection.get_repo_push_events_by_commit_id(
            repo_name, "caa3fdd16ce75c2fb361905e2767602d95f6d33b")

        assert isinstance(
            result_df, pd.DataFrame), "Result should be a pandas DataFrame"

        expected_columns = ['Time', 'Repo', 'Event', 'Metadata']
        assert all(
            column in result_df.columns for column in expected_columns), "DataFrame should have all the expected columns"

        assert result_df['Metadata'].iloc[0] == event_metadata, "Metadata should match the event metadata"

import pytest
import uuid
import boto3

from src.database.db_connection_timeseries import DBConnectionTimeseries

class TestDBConnectionTimeseries:

    DATABASE_NAME = 'DORAStats'
    TABLE_NAME = 'DORARawEventsTest'

    def test_write_timeseries(self):
        db_connection = DBConnectionTimeseries(self.DATABASE_NAME, self.TABLE_NAME)

        random_uuid = str(uuid.uuid4())

        payload = {
            'repo_name': random_uuid,
            'event': 'deploy',
            'metadata': 'test_metadata'
        }

        try:
            db_connection.write_event_to_db(payload)
        except Exception as e:
            pytest.fail(f"Error writing to database: {e}")

        
        res = db_connection.get_all_repo_events(random_uuid)
        assert len(res) == 1, "write_timeseries() should write one event to the database."


    def test_get_deployment_frequency(self):
    
        db_connection = DBConnectionTimeseries(self.DATABASE_NAME, self.TABLE_NAME)

        repos = ["test_repo1", "test_repo2", "test_repo3"]

        res = db_connection.get_days_per_week_with_deploy(repos)
        assert len(res) > 0, "get_deployment_frequency() should return a list of at least one item."

        print (res)

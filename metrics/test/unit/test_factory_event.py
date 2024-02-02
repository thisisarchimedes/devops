import pytest
import os
import pandas as pd
import json

from src.event_processor.events.factory_event import FactoryEvent
from src.event_processor.database.db_connection_fake import DBConnectionFake

from src.event_processor.logger.event_logger_fake import EventLoggerFake


class TestFactoryEvent:

    def test_create_event(self):

        payload = {
            'Time': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            'Repo': 'test_repo',
            'Event': 'push',
            'Metadata': "{'test_metadata'}"
        }

        db_connection = DBConnectionFake(None, None)
        logger = EventLoggerFake()

        event_factory = FactoryEvent(db_connection, logger, 10)
        event = event_factory.create_event(payload)

        assert event is not None, "create_event() should return an event object."
        assert event.get_event_type(
        ) == 'push', "create_event() should return an event object with the correct event type."

    def test_process_test_pass_event(self):

        payload = {
            'Time': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            'Repo': 'test_repo',
            'Event': 'test_pass',
            'Metadata': '{time: 50}'
        }

        db_connection = DBConnectionFake(None, None)
        logger = EventLoggerFake()

        event_factory = FactoryEvent(db_connection, logger, 10)
        event = event_factory.create_event(payload)

        event.process()

        res_df = db_connection.get_repo_events("test_repo")

        metadata_value = str(res_df['Metadata'].iloc[len(res_df.index) - 1])
        assert metadata_value == "{time: 50}" , "process() should write the event to the database."
            
        event_value = str(res_df['Event'].iloc[len(res_df.index) - 1])
        assert event_value == str("test_pass") , "process() should write the event to the database."

        assert event.get_event_type() == 'test_pass', "process() should write the event to the database."


    def test_process_push_event(self):

        payload = {
            'Time': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            'Repo': 'test_repo',
            'Event': 'push',
        }

        db_connection = DBConnectionFake(None, None)
        logger = EventLoggerFake()

        event_factory = FactoryEvent(db_connection, logger, 10)
        event = event_factory.create_event(payload)

        event.process()

        res_df = db_connection.get_repo_events("test_repo")
        repo_name = str(res_df['Repo'].iloc[0])
        assert repo_name == str(
            payload['Repo']), "process() should write the event to the database."

        assert event.get_event_type() == 'push', "process() should write the event to the database."

    def test_process_calc_deploy_frequency_event(self):

        payload = {
            'Time': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            'Repo': 'test_repo',
            'Event': 'calc_deploy_frequency',
        }

        db_connection = DBConnectionFake(None, None)
        logger = EventLoggerFake()

        event_factory = FactoryEvent(db_connection, logger, 10)
        event = event_factory.create_event(payload)

        event.process()

        res_df = db_connection.get_repo_events("test_repo")
        repo_name = str(res_df['Repo'].iloc[0])
        assert repo_name == str(
            payload['Repo']), "process() should write the event to the database."

        assert event.get_event_type(
        ) == 'calc_deploy_frequency', "process() should write the event to the database."
    

    def test_process_deploy_event(self):

        payload = {
            'Time': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            'Repo': 'test_repo',
            'Event': 'deploy',
        }

        db_connection = DBConnectionFake(None, None)
        logger = EventLoggerFake()

        event_factory = FactoryEvent(db_connection, logger, 10)
        event = event_factory.create_event(payload)

        # Use pd.Timestamp for start_date
        start_date = pd.Timestamp.now() - pd.Timedelta(days=90)
        res_df = db_connection.get_deploy_frequency_events_since_date(start_date)
        num_rows_before = len(res_df.index)

        event.process()

        # Use pd.Timestamp for start_date again after processing
        start_date = pd.Timestamp.now() - pd.Timedelta(days=90)
        res_df = db_connection.get_deploy_frequency_events_since_date(start_date)
        num_rows_after = len(res_df.index)

        assert num_rows_after == num_rows_before + \
            1, "process() should write the event to the database."

        
    def test_process_calc_deploy_frequency_event(self):
        payload = {
            'Time': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            'Repo': 'test_repo',
            'Event': 'calc_deploy_frequency',
            'Metadata': '{"deploy_frequency": 12.5}'
        }

        db_connection = DBConnectionFake(None, None)
        logger = EventLoggerFake()

        event_factory = FactoryEvent(db_connection, logger, 10)
        event = event_factory.create_event(payload)

        start_date = pd.Timestamp.now() - pd.Timedelta(days=90)
        res_df = db_connection.get_deploy_frequency_events_since_date(
            start_date)
        num_rows_before = len(res_df.index)

        event.process()

        start_date = pd.Timestamp.now() - pd.Timedelta(days=90)
        res_df = db_connection.get_deploy_frequency_events_since_date(
            start_date)
        num_rows_after = len(res_df.index)

        assert num_rows_after == num_rows_before + \
            1, "process() should write the event to the database."


    def test_test_run_event(self):

        payload = {
            'Time': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            'Repo': 'test_repo',
            'Event': 'test_run',
            'Metadata': '{"pass": true, "time": 50}'
        }

        db_connection = DBConnectionFake(None, None)
        logger = EventLoggerFake()

        event_factory = FactoryEvent(db_connection, logger, 10)
        event = event_factory.create_event(payload)

        event.process()

        res_df = db_connection.get_repo_events("test_repo")

        metadata_value = str(res_df['Metadata'].iloc[len(res_df.index) - 1])
        assert metadata_value == '{"pass": true, "time": 50}' , "process() should write the event to the database."
            
        event_value = str(res_df['Event'].iloc[len(res_df.index) - 1])
        assert event_value == str("test_run") , "process() should write the event to the database."

        assert event.get_event_type() == 'test_run', "process() should write the event to the database."

     
    def test_process_deploy_event_get_commit_ids(self):

        db_connection = DBConnectionFake(None, None)
        logger = EventLoggerFake()
        event_factory = FactoryEvent(db_connection, logger, 10)

        payload = {
            'Time': '2024-01-07 17:31:41.449864',
            'Repo': 'test_repo',
            'Event': 'push',
            'Metadata': '{"commit_id": 100}'
        }
        event_push_1 = event_factory.create_event(payload)
        event_push_1.process()

        payload = {
            'Time': '2024-01-03 17:31:41.449864',
            'Repo': 'test_repo',
            'Event': 'push',
            'Metadata': '{"commit_id": 200}'
        }
        event_push_2 = event_factory.create_event(payload)
        event_push_2.process()

        payload = {
            'Time': '2024-01-08 17:31:41.449864',
            'Repo': 'test_repo',
            'Event': 'push',
            'Metadata': '{"commit_id": 300}'
        }
        event_push_3 = event_factory.create_event(payload)
        event_push_3.process()

        payload = {
            'Time': '2024-01-09 17:31:41.449864',
            'Repo': 'test_repo',
            'Event': 'deploy',
            'Metadata': '{"commit_ids": [100,200,300]}'
        }
        event_deploy = event_factory.create_event(payload)
        
        event_deploy.process()
        # commit 1: 2 days
        # commit 2: 6 days
        # commit 3: 1 day
        # median: 2 days
        
        df = db_connection.get_most_recent_event('calc_deploy_lead_time')
        
        # metadata --> {"deploy_lead_time": "2"}
        metadata = df['Metadata'].iloc[0]
        metadata_dict = json.loads(metadata)
        print(metadata_dict)
        deploy_median_lead_time = metadata_dict['deploy_lead_time']        

        assert deploy_median_lead_time == 2, "process() should write the event to the database."
        
    
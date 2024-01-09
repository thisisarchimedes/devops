import pytest
from datetime import datetime, timedelta
import os
import pandas as pd

from src.events.factory_event import FactoryEvent
from src.database.db_connection_fake import DBConnectionFake

class TestFactoryEvent:

    def test_create_event(self):
            
        payload = {
            'repo_name': 'test_repo',
            'event': 'push',
            'metadata': {'test_metadata'}
        }

        db_connection = DBConnectionFake()
            
        event_factory = FactoryEvent(db_connection)
        event = event_factory.create_event(payload)

        assert event is not None, "create_event() should return an event object."
        assert event.get_event_type() == 'push', "create_event() should return an event object with the correct event type."


    def test_process_test_pass_event(self):
                
        payload = {
            'repo_name': 'test_repo',
            'event': 'test_pass',
            'metadata': {'time: 50'}
        }
    
        db_connection = DBConnectionFake("db_test_event_factory", "test_process_test_pass_event")
            
        event_factory = FactoryEvent(db_connection)
        event = event_factory.create_event(payload)

        event.process()

        res_df = db_connection.get_all_repo_events("test_repo")
        metadata_value = str(res_df['metadata'].iloc[0])
        assert metadata_value == str(payload['metadata']), "process() should write the event to the database."

        assert event.get_event_type() == 'test_pass', "process() should write the event to the database."

    
    def test_process_push_event(self):
                
        payload = {
            'repo_name': 'test_repo',
            'event': 'push',
        }

        db_connection = DBConnectionFake("db_test_event_factory", "test_process_push_event")
            
        event_factory = FactoryEvent(db_connection)
        event = event_factory.create_event(payload)

        event.process()

        res_df = db_connection.get_all_repo_events("test_repo")
        repo_name = str(res_df['repo_name'].iloc[0])
        assert repo_name == str(payload['repo_name']), "process() should write the event to the database."

        assert event.get_event_type() == 'push', "process() should write the event to the database."

    
    def test_process_deploy_event(self):
                
        payload = {
            'repo_name': 'test_repo',
            'event': 'deploy',
        }

        db_connection = DBConnectionFake("db_test_event_factory", "test_process_deploy_event")
        db_connection.set_db_read_only_flag(True)
            
        event_factory = FactoryEvent(db_connection)
        event = event_factory.create_event(payload)

        start_date = datetime.now() - timedelta(days=90)
        res_df = db_connection.get_deploy_frequency_reports_since_date(start_date)
        num_rows_before = len(res_df.index)

        event.process()

        start_date = datetime.now() - timedelta(days=90)
        res_df = db_connection.get_deploy_frequency_reports_since_date(start_date)
        num_rows_after = len(res_df.index)
        
        assert num_rows_after == num_rows_before + 1, "process() should write the event to the database."
       
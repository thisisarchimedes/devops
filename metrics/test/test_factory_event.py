import pytest
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

        assert event.get_event_type() == 'test_pass', "process() should write the event to the database."
        assert db_connection.get_all_repo_events("test_repo") == [str(payload)], "process() should write the event to the database."
    
    def test_process_push_event(self):
                
        payload = {
            'repo_name': 'test_repo',
            'event': 'push',
        }

        db_connection = DBConnectionFake("db_test_event_factory", "test_process_push_event")
            
        event_factory = FactoryEvent(db_connection)
        event = event_factory.create_event(payload)

        event.process()

        assert event.get_event_type() == 'push', "process() should write the event to the database."
        assert db_connection.get_all_repo_events("test_repo") == [str(payload)], "process() should write the event to the database."

    def test_process_deploy_event(self):
                
        payload = {
            'repo_name': 'test_repo',
            'event': 'deploy',
        }

        db_connection = DBConnectionFake("db_test_event_factory", "test_process_deploy_event")
        db_connection.set_db_read_only_flag(True)
            
        event_factory = FactoryEvent(db_connection)
        event = event_factory.create_event(payload)

        event.process()

        assert event.get_event_type() == 'push', "process() should write the event to the database."
        assert db_connection.get_all_repo_events("test_repo") == [str(payload)], "process() should write the event to the database."



        
        
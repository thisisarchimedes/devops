import pytest
import json
import os
from src.event_processor import EventProcessor
from src.database.db_connection_fake import DBConnectionFake

class TestEventProcessor:

    def test_is_unautherized(self):

        event_processor = EventProcessor("SECRET_TOKEN", None)

        res = event_processor.is_autherized("INVALID_TOKEN")

        assert res == False, "is_autherized() should return False when no auth token is provided."


    def test_payload_invalid_event(self):

        event_processor = EventProcessor("SECRET_TOKEN", None)

        payload = {
            'repo_name': 'test_repo',
            'event': 'invalid',
            'metadata': 'test_metadata'
        }

        res = event_processor.is_payload_valid(payload)
        assert res == False, "is_payload_valid() should return False when event type is invalid."

    def test_payload_event_missing(self):

        event_processor = EventProcessor("SECRET_TOKEN", None)

        payload = {
            'repo_name': 'test_repo',
            'metadata': 'test_metadata'
        }

        res = event_processor.is_payload_valid(payload)
        assert res == False, "test_payload_event_missing() should return False when event type is invalid."

    def test_payload_valid_without_metadata(self):

        event_processor = EventProcessor("SECRET_TOKEN", None)

        payload = {
            'repo_name': 'test_repo',
            'event': 'push',
        }

        res = event_processor.is_payload_valid(payload)
        assert res == True, "test_payload_valid_without_metadata() should return True when payload is valid."


    def test_write_event_to_db(self):

        db_connection = DBConnectionFake()
        secret_token = os.getenv('SECRET_TOKEN')
        event_processor = EventProcessor(secret_token, db_connection)

        payload = {
            'repo_name': 'test_repo',
            'event': 'push',
            'metadata': 'test_metadata'
        }

        try:
            event_processor.write_event_to_db(payload)
        except:
            pytest.fail("write_event_to_db() should not throw an error when payload is valid.")

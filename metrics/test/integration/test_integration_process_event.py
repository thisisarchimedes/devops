import pytest
from datetime import datetime

from src.event_processor.entry_local import entry_point_local


class TestIntegrationProcessEvent():

    def test_process_event_deploy(self):

        event_payload = {
            'Time': datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            'Repo': 'test_repo',
            'Event': 'deploy',
            'Metadata': '{"commit_ids": [1,2,3]}'
        }

        entry_point_local(event_payload)

    def test_process_event_calc_frequency(self):

        event_payload = {
            'Time': datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            'Repo': 'test_repo',
            'Event': 'calc_deploy_frequency',
            'Metadata': '{"deploy_frequency": 2.5}'
        }

        entry_point_local(event_payload)

    def test_process_event_push(self):

        event_payload = {
            'Time': datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            'Repo': 'test_repo',
            'Event': 'push',
        }

        entry_point_local(event_payload)

    def test_process_event_test_pass(self):

        event_payload = {
            'Time': datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            'Repo': 'test_repo',
            'Event': 'test_pass',
            'Metadata': '{"time": 50}'
        }

        entry_point_local(event_payload)

    def test_process_event_test_run(self):

        event_payload = {
            'Time': datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            'Repo': 'test_repo',
            'Event': 'test_run',
            'Metadata': '{"pass": true, "time": 50}'
        }

        entry_point_local(event_payload)

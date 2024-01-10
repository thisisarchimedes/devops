import pytest
from datetime import datetime

from src.event_processor.lambda_entry import process_new_event

class TestIntegrationProcessEvent():

    def test_process_event(self):
        
        event_payload = {
            'Time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Repo': 'test_repo',
            'Event': 'calc_deploy_frequency',
            'Metadata': '{deploy_frequency: 7.5}'
        }
        
        process_new_event(event_payload)
        
        
import pytest
from datetime import datetime

from src.event_processor.entrance_local_process_event import entry_point_local

class TestIntegrationProcessEvent():

    def test_process_event(self):
        
        event_payload = {
            'Time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Repo': 'test_repo',
            'Event': 'calc_deploy_frequency',
            'Metadata': '{deploy_frequency: 8.5}'
        }
        
        entry_point_local(event_payload)
        
        
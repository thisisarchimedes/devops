import os
import uuid
import requests
import pytest
from datetime import datetime, timedelta

import pandas as pd
from dotenv import load_dotenv

from src.event_processor.logger.event_logger import EventLogItem
from src.event_processor.logger.event_logger_new_relic import EventLoggerNewRelic


class TestEventLoggerNewRelic():

    def test_send_event_to_logger(self) -> None:

        event_logger = EventLoggerNewRelic()
        unique_id = str(uuid.uuid4())
        event = pd.DataFrame({
            'Time': datetime.now(),
            'Repo': 'test_logger',
            'Event': 'deploy',
            'Metadata': {'test_id': unique_id},
        })
        
        event_log_item = event_logger.get_event_log_item_from_event(event)
        event_logger.send_event_to_logger(event_log_item)

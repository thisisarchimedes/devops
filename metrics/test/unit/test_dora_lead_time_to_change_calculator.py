import pytest
from datetime import datetime
import pandas as pd
from src.event_processor.database.db_connection_fake import DBConnectionFake
from src.event_processor.events.factory_event import FactoryEvent
from src.event_processor.logger.event_logger_fake import EventLoggerFake

from src.event_processor.calculations.dora_lead_time_to_change_calculator import DORALeadTimeToChangeCalculator

class TestDORALeadTimeToChangeCalculator:

    def prep_test_data(self) -> None:

        date_format = "%Y-%m-%d %H:%M:%S"

        payload1 = {
            'Time': datetime.strptime("2024-01-09", "%Y-%m-%d").strftime(date_format),
            'Repo': 'test_repo',
            'Event': 'push',
            'Metadata': '{"commit_id": "1"}'
        }
        payload2 = {
            'Time': datetime.strptime("2024-01-12", "%Y-%m-%d").strftime(date_format),
            'Repo': 'test_repo',
            'Event': 'push',
            'Metadata': '{"commit_id": "2"}'
        }
        payload3 = {
            'Time': datetime.strptime("2024-01-19", "%Y-%m-%d").strftime(date_format),
            'Repo': 'test_repo',
            'Event': 'push',
            'Metadata': '{"commit_id": "3"}'
        }


        db_connection = DBConnectionFake(None, None)
        logger = EventLoggerFake()

        event_factory = FactoryEvent(db_connection, logger, 10)
        
        event1 = event_factory.create_event(payload1)
        event2 = event_factory.create_event(payload2)
        event3 = event_factory.create_event(payload3)
        
        self.push_events = [event1, event2, event3]
        self.deploy_event_date = "2024-01-20"

        # commit 1: 11 days
        # commit 2: 8 days
        # commit 3: 1 day
        # median: 8 days


    def test_calculate_median_day_lead_time_for_deploy(self):

        self.prep_test_data()

        lead_time_calculator = DORALeadTimeToChangeCalculator()

        median_lead_time = lead_time_calculator.calculate_median_day_lead_time_for_deploy(
            self.push_events,
            self.deploy_event_date
        )

        assert median_lead_time == 8, "Median lead time should be 8 days"

       
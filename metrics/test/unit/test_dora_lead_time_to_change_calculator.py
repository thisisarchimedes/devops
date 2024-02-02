import pytest
import pandas as pd
from src.event_processor.database.db_connection_fake import DBConnectionFake
from src.event_processor.events.factory_event import FactoryEvent
from src.event_processor.logger.event_logger_fake import EventLoggerFake
from src.event_processor.calculations.dora_lead_time_to_change_calculator import DORALeadTimeToChangeCalculator

class TestDORALeadTimeToChangeCalculator:

    def prep_test_data(self) -> None:

        # Convert datetime string directly to pd.Timestamp without intermediate datetime object
        payload1 = {
            'Time': pd.Timestamp("2024-01-09 19:41:03.154531"),
            'Repo': 'test_repo',
            'Event': 'push',
            'Metadata': '{"commit_id": "1"}'
        }
        payload2 = {
            'Time': pd.Timestamp("2024-01-12 19:41:03.154531"),
            'Repo': 'test_repo',
            'Event': 'push',
            'Metadata': '{"commit_id": "2"}'
        }
        payload3 = {
            'Time': pd.Timestamp("2024-01-19 19:41:03.154531"),
            'Repo': 'test_repo',
            'Event': 'push',
            'Metadata': '{"commit_id": "3"}'
        }
        
        self.push_events = [pd.DataFrame([payload1]), pd.DataFrame([payload2]), pd.DataFrame([payload3])]
        self.deploy_event_date = pd.Timestamp("2024-01-20 19:41:03.154531")

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

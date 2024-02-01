from datetime import datetime, timedelta
import pandas as pd
import json

from src.event_processor.events.event import Event
from src.event_processor.calculations.dora_deploy_frequency_calculator import DORADeployFrequencyCalculator
from src.event_processor.calculations.dora_lead_time_to_change_calculator import DORALeadTimeToChangeCalculator

from src.event_processor.database.db_connection import DBConnection
from src.event_processor.logger.event_logger import EventLogger

class EventDeploy(Event):

    def __init__(self, 
                 payload: dict, 
                 db_connection: DBConnection, 
                 logger: EventLogger, 
                 deploy_frequency_timewindow_days: int) -> None:
        super().__init__(payload, db_connection, logger)
        self.deploy_frequency_timewindow_days = deploy_frequency_timewindow_days

    def process(self) -> None:
        self._write_event_to_db()
        self._log_event()
        
        deploy_frequency = self._calculate_deploy_frequency()
        self._report_deploy_frequency(deploy_frequency)

        try:
            self._calculate_median_lead_time_for_deploy()
        except ValueError as e:
            pass

    def _calculate_median_lead_time_for_deploy(self) -> int:

        # event meta data is '{"commit_ids": ["6074dabea1a77f5040cdd3349b66aa03b2db208a","d6316a779419bff4b9a46c544799e6cf2525bb13"]}'    
        # get commit ids from meta data

        metadata = self.get_metadata()
        if metadata is None:
            exception_message = "EventDeploy: Metadata is None"
            raise ValueError(exception_message)

        
        metadata_dict = json.loads(metadata)
        if not isinstance(metadata_dict['commit_ids'], list):
            exception_message = "EventDeploy: Metadata is not a list"
            raise ValueError(exception_message)
        
        commit_ids = metadata_dict['commit_ids']

        push_events = []
        for commit_id in commit_ids:
            event_df = self.db_connection.get_repo_push_events_by_commit_id(self.get_repo_name(), commit_id)
            push_events.append(event_df)

        calc = DORALeadTimeToChangeCalculator()
        median_lead_time = calc.calculate_median_day_lead_time_for_deploy(
            push_events,
            self.get_time()
        )

        metadata = json.dumps({"deploy_lead_time": median_lead_time})
        event = {
            'Time': datetime.now(),
            'Repo': self.get_repo_name(),
            'Event': 'calc_deploy_lead_time',
            'Metadata': metadata
        }
        
        event_df = pd.DataFrame([event])
        self.db_connection.write_event_to_db(event_df)
        res = self.logger.get_event_log_item_from_df_event(event_df)
        self.logger.send_event_to_logger(res)

            


    def _write_event_to_db(self):
        self.db_connection.write_event_to_db(self.payload)

    def _log_event(self):
        res = self.logger.get_event_log_item_from_df_event(self.payload)
        self.logger.send_event_to_logger(res)

    def _calculate_deploy_frequency(self) -> float:
        start_date = datetime.now() - timedelta(days=self.deploy_frequency_timewindow_days)
        end_date = datetime.now()
        daily_deploy_volume_df = self.db_connection.get_daily_deploy_volume(None)

        dora_deploy_frequency_calculator = DORADeployFrequencyCalculator()
        return dora_deploy_frequency_calculator.get_deployment_frequency(
            daily_deploy_volume=daily_deploy_volume_df,
            start_date=start_date,
            end_date=end_date
        )

    def _report_deploy_frequency(self, deploy_frequency: float):
        metadata = json.dumps({"deploy_frequency": deploy_frequency})
        event = {
            'Time': datetime.now(),
            'Repo': 'ALL',
            'Event': 'calc_deploy_frequency',
            'Metadata': metadata
        }
        
        event_df = pd.DataFrame([event])
        self.db_connection.write_event_to_db(event_df)
        res = self.logger.get_event_log_item_from_df_event(event_df)
        self.logger.send_event_to_logger(res)

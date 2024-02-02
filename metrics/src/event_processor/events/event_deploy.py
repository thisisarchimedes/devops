import pandas as pd
import json

from src.event_processor.events.event import Event
from src.event_processor.events.event_types import EventTypes
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
        self._calculate_and_report_dora_metrics()

    def _write_event_to_db(self):
        self.db_connection.write_event_to_db(self.payload)

    def _log_event(self):
        res = self.logger.get_event_log_item_from_df_event(self.payload)
        self.logger.send_event_to_logger(res)

    def _calculate_and_report_dora_metrics(self) -> None:
        deploy_frequency = self._calculate_deploy_frequency()
        self._report_deploy_frequency(deploy_frequency)

        # if no commits - skip lead time calculation
        #try:
        print(f'_calculate_and_report_dora_metrics - 0')
        median_lead_time = self._calculate_median_lead_time_for_deploy()
        print(
            f'_calculate_and_report_dora_metrics - 1 median_lead_time: {median_lead_time}')
        self._report_median_lead_time(median_lead_time)
        print(f'_calculate_and_report_dora_metrics - 2')
        #except Exception as e:
         #   print(f'Warning: problem while calculating median lead time: {e}')

    def _calculate_deploy_frequency(self) -> float:
        start_date = pd.Timestamp.now() - pd.Timedelta(days=self.deploy_frequency_timewindow_days)
        end_date = pd.Timestamp.now()
        daily_deploy_volume_df = self.db_connection.get_daily_deploy_volume(
            None)
        dora_deploy_frequency_calculator = DORADeployFrequencyCalculator()
        return dora_deploy_frequency_calculator.get_deployment_frequency(daily_deploy_volume_df, start_date, end_date)

    def _report_deploy_frequency(self, deploy_frequency: float):
        event_dict = self._create_event_dict(EventTypes.CALC_DEPLOY_FREQUENCY, {
                                             "deploy_frequency": deploy_frequency})
        self._write_and_log_event(event_dict)

    def _calculate_median_lead_time_for_deploy(self) -> int:
        print(f'_calculate_median_lead_time_for_deploy - 0')
        metadata_dict = self._extract_metadata_dict()
        print(
            f'_calculate_median_lead_time_for_deploy - 1 metadata_dict: {metadata_dict}')
        commit_ids = self._validate_and_get_commit_ids(metadata_dict)
        print(
            f'_calculate_median_lead_time_for_deploy - 2 commit_ids: {commit_ids}')
        push_events = self._get_push_events(commit_ids)
        print(
            f'_calculate_median_lead_time_for_deploy - 3 push_events: {push_events}')
        res = self._calculate_median_lead_time(push_events)
        print(f'_calculate_median_lead_time_for_deploy - 4 res: {res}')
        return res

    def _report_median_lead_time(self, median_lead_time: int):
        event_dict = self._create_event_dict(EventTypes.CALC_DEPLOY_LEAD_TIME, {
                                             "deploy_lead_time": median_lead_time})
        self._write_and_log_event(event_dict)

    def _create_event_dict(self, event_type: str, metadata: dict) -> dict:
        """Create an event dictionary."""
        return {
            'Time': pd.Timestamp.now(),
            'Repo': self.get_repo_name(),
            'Event': event_type,
            'Metadata': json.dumps(metadata)
        }

    def _write_and_log_event(self, event_dict: dict) -> None:
        """Write the event to the database and log it."""
        event_df = pd.DataFrame([event_dict])
        self.db_connection.write_event_to_db(event_df)
        res = self.logger.get_event_log_item_from_df_event(event_df)
        self.logger.send_event_to_logger(res)

    def _extract_metadata_dict(self) -> dict:
        metadata = self.get_metadata()
        if metadata is None:
            raise ValueError("EventDeploy: Metadata is None")
        return json.loads(metadata)

    def _validate_and_get_commit_ids(self, metadata_dict: dict) -> [str]:
        if 'commit_ids' not in metadata_dict or not isinstance(metadata_dict['commit_ids'], list):
            raise ValueError(
                "EventDeploy: 'commit_ids' not found or is not a list in Metadata")
        return metadata_dict['commit_ids']

    def _get_push_events(self, commit_ids: [str]) -> [pd.DataFrame]:
        push_events = []
        for commit_id in commit_ids:
            event_df = self.db_connection.get_repo_push_events_by_commit_id(
                self.get_repo_name(), str(commit_id))
            push_events.append(event_df)
        return push_events

    def _calculate_median_lead_time(self, push_events: list[pd.DataFrame]) -> int:
        print(f'_calculate_median_lead_time - 0  \n{push_events}\n')
        calc = DORALeadTimeToChangeCalculator()
        print(f'_calculate_median_lead_time - 1')
        tmp = self.get_time()
        print(f'_calculate_median_lead_time - 1.5')
        res = calc.calculate_median_day_lead_time_for_deploy(push_events, tmp)
        print(f'_calculate_median_lead_time - 2 res: {res}')
        return res

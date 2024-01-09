
from dataclasses import dataclass
import pandas as pd


DEVOPS_METRICS_SERVICE_LABEL = 'devops-metrics'


@dataclass
class EventLogItem():

    event: pd.DataFrame
    message: str = ''
    service: str = DEVOPS_METRICS_SERVICE_LABEL


class EventLogger():

    def send_event_to_logger(self, event_log_item: EventLogItem) -> None:
        pass

    def get_event_log_item_from_df_event(self, event: pd.DataFrame) -> EventLogItem:
        return EventLogItem(
            event=event,
            message=f'Repo: {event["Repo"].iloc[0]} ; Event: {event["Event"].iloc[0]}',
            service=DEVOPS_METRICS_SERVICE_LABEL,
        )


from dataclasses import dataclass
import pandas as pd
import json

DEVOPS_METRICS_SERVICE_LABEL = 'devops-metrics'


@dataclass
class EventLogItem():

    event: str = ''
    message: str = ''
    service: str = DEVOPS_METRICS_SERVICE_LABEL


class EventLogger():

    def send_event_to_logger(self, event_log_item: EventLogItem) -> None:
        pass

    def get_event_log_item_from_df_event(self, event: pd.DataFrame) -> EventLogItem:

        # DF always has one row
        event_item_json = event.iloc[0].to_json(orient='index')

        return EventLogItem(
            event=event_item_json,
            message=f'Repo: {event["Repo"].iloc[0]} ; Event: {event["Event"].iloc[0]}',
            service=DEVOPS_METRICS_SERVICE_LABEL,
        )

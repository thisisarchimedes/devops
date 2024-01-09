
from dataclasses import dataclass
import pandas as pd


DEVOPS_METRICS_SERVICE_LABEL = 'devops-metrics'

@dataclass
class EventLogItem():
    
    environment: str
    event: pd.DataFrame
    message: str = ''
    service: str = DEVOPS_METRICS_SERVICE_LABEL


class EventLogger():

    def send_event_to_logger(self, event: pd.DataFrame) -> None:
        pass

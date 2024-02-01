from datetime import datetime
import pandas as pd

from src.event_processor.events.event_push import EventPush

class DORALeadTimeToChangeCalculator():

    def calculate_median_day_lead_time_for_deploy(self, push_events: pd.DataFrame, deploy_event_date: str) -> int:
        deploy_date = self._parse_date(deploy_event_date)        
        lead_times = self._calculate_lead_times(push_events, deploy_date)
        
        return self._calculate_median(lead_times)
    

    def _parse_date(self, date_str: str, date_format: str = "%Y-%m-%d") -> datetime:
        return datetime.strptime(date_str, date_format)

    def _calculate_lead_times(self, push_events: pd.DataFrame, deploy_date: datetime) -> [int]:
        lead_times = []
        for _, event in push_events.iterrows():
            # Extracting the 'Time' value from each row.
            push_date_str = event['Time']
            push_date = self._parse_date(push_date_str, "%Y-%m-%d %H:%M:%S")
            lead_time = (deploy_date - push_date).days
            lead_times.append(lead_time)
        return lead_times



    @staticmethod
    def _calculate_median(values: [int]) -> float:
        values.sort()
        n = len(values)
        mid = n // 2
        if n % 2 == 0:
            return (values[mid - 1] + values[mid]) / 2
        else:
            return values[mid]

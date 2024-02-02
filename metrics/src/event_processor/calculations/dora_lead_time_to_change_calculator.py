import pandas as pd

class DORALeadTimeToChangeCalculator():

    def calculate_median_day_lead_time_for_deploy(self, push_events: list[pd.DataFrame], deploy_event_date: pd.Timestamp) -> float:
        """Calculate the median lead time for deployment based on push events and deployment date."""
        lead_times = self._calculate_lead_times(push_events, deploy_event_date)
        return self._calculate_median(lead_times)
    

    def _calculate_lead_times(self, push_events: list[pd.DataFrame], deploy_date: pd.Timestamp) -> list[int]:
        """Calculate lead times for each push event."""
        lead_times = []
        for event_df in push_events:
            if not event_df.empty and 'Time' in event_df.columns:
                push_date = pd.to_datetime(event_df['Time'].iloc[0])  # Convert the 'Time' column to pd.Timestamp
                lead_time = (deploy_date - push_date).days
                lead_times.append(lead_time)
        return lead_times

    @staticmethod
    def _calculate_median(values: list[int]) -> float:
        """Calculate the median of a list of values."""
        values.sort()
        n = len(values)
        mid = n // 2
        if n % 2 == 0:
            return (values[mid - 1] + values[mid]) / 2
        else:
            return values[mid]

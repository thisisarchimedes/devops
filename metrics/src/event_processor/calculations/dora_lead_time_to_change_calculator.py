import pandas as pd


class DORALeadTimeToChangeCalculator():

    def calculate_median_day_lead_time_for_deploy(self, push_events: list[pd.DataFrame], deploy_event_date: pd.Timestamp) -> float: 
        lead_times = self._calculate_lead_times(push_events, deploy_event_date) 
        res = self._calculate_median(lead_times)
        return res

    def _calculate_lead_times(self, push_events: list[pd.DataFrame], deploy_date: pd.Timestamp) -> list[int]:
        lead_times = []
        for event_df in push_events:
            if not event_df.empty and 'Time' in event_df.columns:
                push_date = pd.to_datetime(event_df['Time'].iloc[0])

                # Ensure push_date has the same timezone as deploy_date
                if deploy_date.tz is not None:
                    push_date = push_date.tz_localize(deploy_date.tz)

                # If deploy_date is naive, make push_date naive as well
                elif deploy_date.tz is None and push_date.tz is not None:
                    push_date = push_date.tz_localize(None)

                lead_time = (deploy_date - push_date).days
                lead_times.append(lead_time)

        return lead_times


    @staticmethod
    def _calculate_median(values: list[int]) -> float:
        if not values:
            return float('nan')

        values.sort()
        n = len(values)
        mid = n // 2
        if n % 2 == 0:
            return (values[mid - 1] + values[mid]) / 2
        else:
            return values[mid]

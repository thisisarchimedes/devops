import pandas as pd


class DORALeadTimeToChangeCalculator:

    def calculate_median_day_lead_time_for_deploy(self, push_events: list[pd.DataFrame], deploy_event_date: pd.Timestamp) -> float:
        lead_times = self._calculate_lead_times_for_all_pushes(push_events, deploy_event_date)
        median = self._calculate_median(lead_times)

        return median

    def _calculate_lead_times_for_all_pushes(self, push_events: list[pd.DataFrame], deploy_date: pd.Timestamp) -> list[int]:
        lead_times = []
        for event_df in push_events:
            if not self._is_valid_event(event_df):
                continue

            lead_time = self._calculate_lead_time(event_df, deploy_date)
            lead_times.append(lead_time)

        return lead_times

    def _calculate_lead_time(self, event_df: pd.DataFrame, deploy_date: pd.Timestamp) -> int:
        push_date = self._normalize_push_date(event_df, deploy_date)
        return self._compute_lead_time(push_date, deploy_date)

    def _is_valid_event(self, event_df: pd.DataFrame) -> bool:
        return not event_df.empty and 'Time' in event_df.columns

    def _normalize_push_date(self, event_df: pd.DataFrame, deploy_date: pd.Timestamp) -> pd.Timestamp:
        push_date = pd.to_datetime(event_df['Time'].iloc[0])
        push_date = self._adjust_timezone(push_date, deploy_date)
        return push_date

    def _adjust_timezone(self, push_date: pd.Timestamp, deploy_date: pd.Timestamp) -> pd.Timestamp:
        if deploy_date.tz is not None:
            return push_date.tz_localize(deploy_date.tz, copy=True) 
        elif deploy_date.tz is None and push_date.tz is not None:
            return push_date.tz_localize(None, copy=True)
        return push_date

    def _compute_lead_time(self, push_date: pd.Timestamp, deploy_date: pd.Timestamp) -> int:
        return (deploy_date - push_date).days

    def _calculate_median(self, values: list[int]) -> float:
        if not values:
            return float('nan')

        values.sort()
        n = len(values)
        mid = n // 2
        if n % 2 == 0:
            return (values[mid - 1] + values[mid]) / 2
        else:
            return values[mid]

from datetime import datetime, timedelta, date, time
import pandas as pd

class DORADeployFrequencyCalculator():
    def __init__(self):
        pass

    def get_days_with_deploy_per_week_from_daily_deploy_volume(self, daily_deploy_volume: pd.DataFrame, start_date: date, end_date: date) -> pd.DataFrame:
        # Convert 'Day' column to datetime and filter out weekends
        daily_deploy_volume['Day'] = pd.to_datetime(daily_deploy_volume['Day'])
        daily_deploy_volume = daily_deploy_volume[daily_deploy_volume['Day'].dt.weekday < 5]

        # Convert any non-zero DeployCount to 1
        daily_deploy_volume['DeployCount'] = daily_deploy_volume['DeployCount'].apply(lambda x: 1 if x >= 1 else 0)

        # Adjust the start_date to the nearest past Monday
        start_date = datetime.combine(start_date, time.min)
        if start_date.weekday() != 0:
            start_date -= timedelta(days=start_date.weekday())

        # Adjust the end_date to the nearest Sunday
        end_date = datetime.combine(end_date, time.min)
        if end_date.weekday() != 6:
            end_date += timedelta(days=6 - end_date.weekday())

        # Create a date range with weekly frequency starting from Mondays
        date_range = pd.date_range(start=start_date, end=end_date, freq='W-MON')

        # Map each day to the Monday of its week
        daily_deploy_volume['WeekStart'] = daily_deploy_volume['Day'].apply(lambda x: x - timedelta(days=x.weekday()))

        # Group by 'WeekStart' and sum the 'DeployCount' (which is now either 0 or 1)
        weekly_deploy_count = daily_deploy_volume.groupby('WeekStart')['DeployCount'].sum()

        # Create the output DataFrame
        output = pd.DataFrame({'Week': date_range})
        output['DaysWithDeploy'] = output['Week'].apply(lambda d: weekly_deploy_count.get(d, 0))

        return output
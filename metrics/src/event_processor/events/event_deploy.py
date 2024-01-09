from datetime import datetime, timedelta
import pandas as df

from src.event_processor.events.event import Event
from src.event_processor.calculations.dora_deploy_frequency_calculator import DORADeployFrequencyCalculator

class EventDeploy(Event):
    
    def __init__(self, payload: dict, db_connection) -> None:
        super().__init__(payload, db_connection)

        self.deploy_frequency_timewindow_days = 90

    def process(self) -> None:

        self.db_connection.write_event_to_db(self.payload)

        daily_deploy_volume_df = self.db_connection.get_daily_deploy_volume()
        dora_deploy_frequency_calculator = DORADeployFrequencyCalculator()
        start_date = datetime.now() - timedelta(days=self.deploy_frequency_timewindow_days)
        end_date = datetime.now()

        print(daily_deploy_volume_df)
        
        deploy_frequency = dora_deploy_frequency_calculator.get_deployment_frequency(daily_deploy_volume=daily_deploy_volume_df,
                                                                  start_date=start_date,
                                                                  end_date=end_date)

        event = {
            'Time': datetime.now(),
            'Repo': 'ALL',
            'Event': 'calc_deploy_frequency',
            'Metadata': {'deploy_frequency': deploy_frequency}
        }
        event_df = df.DataFrame(event)
        self.db_connection.write_event_to_db(event_df)

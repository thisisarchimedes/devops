import datetime

from src.events.event import Event
from src.calculations.dora_deploy_frequency_calculator import DORADeployFrequencyCalculator

class EventCalcDeployFrequency(Event):
    
    def process(self) -> None:

        self.db_connection.write_event_to_db(self.payload)

        

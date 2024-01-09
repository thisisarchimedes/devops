
from src.event_processor.database.db_connection import DBConnection

from src.event_processor.events.event import Event
from src.event_processor.events.event_push import EventPush
from src.event_processor.events.event_test_pass import EventTestPass
from src.event_processor.events.event_deploy import EventDeploy
from src.event_processor.events.event_calc_deploy_freq import EventCalcDeployFrequency

class FactoryEvent():

    def __init__(self, db_connection: DBConnection) -> None:
        self.db_connection = db_connection

    def create_event(self, payload: dict) -> Event:
            
        if payload['Event'] == 'push':
            event = EventPush(payload, self.db_connection)
        elif payload['Event'] == 'test_pass':
            event = EventTestPass(payload, self.db_connection)
        elif payload['Event'] == 'deploy':
            event = EventDeploy(payload, self.db_connection)
        elif payload['Event'] == 'calc_deploy_frequency':
            event = EventCalcDeployFrequency(payload, self.db_connection)
        else:
            raise Exception("Invalid event type.")
        
        return event

from src.database.db_connection import DBConnection

from src.events.event import Event
from src.events.event_push import EventPush
from src.events.event_test_pass import EventTestPass

class FactoryEvent():

    def __init__(self, db_connection: DBConnection) -> None:
        self.db_connection = db_connection

    def create_event(self, payload: dict) -> Event:
            
        if payload['event'] == 'push':
            event = EventPush(payload, self.db_connection)
        elif payload['event'] == 'test_pass':
            event = EventTestPass(payload, self.db_connection)
        else:
            raise Exception("Invalid event type.")
        
        return event
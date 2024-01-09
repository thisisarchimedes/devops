from src.event_processor.events.event import Event

class EventTestPass(Event):

    def process(self) -> None:
        self.db_connection.write_event_to_db(self.payload)

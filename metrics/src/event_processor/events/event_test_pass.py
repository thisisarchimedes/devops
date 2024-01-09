from src.event_processor.events.event import Event

class EventTestPass(Event):

    def process(self) -> None:
        self.db_connection.write_event_to_db(self.payload)
        
        res = self.logger.get_event_log_item_from_event(self.payload)
        self.logger.send_event_to_logger(res)
import os

from src.event_processor.config.config import Config
from src.event_processor.config.config_local import ConfigLocal
from src.event_processor.config.payload_validator import PayloadValidator
from src.event_processor.database.db_connection_timeseries import DBConnectionTimeseries
from src.event_processor.logger.event_logger_new_relic import EventLoggerNewRelic
from src.event_processor.events.factory_event import FactoryEvent

def entry_point_local(event_payload: dict):
    
    if PayloadValidator().is_payload_valid(event_payload) == False:
        raise Exception('Invalid payload')
    
    process_new_event(event_payload, ConfigLocal())


def process_new_event(event_payload: dict, config: Config) -> None:
      
    db_connection = DBConnectionTimeseries(config.get_db_name(), config.get_db_table_name())
    event_logger = EventLoggerNewRelic(config.get_logger_api_key())

    factory_event = FactoryEvent(db_connection, event_logger)
    event = factory_event.create_event(event_payload)
    event.process()
    

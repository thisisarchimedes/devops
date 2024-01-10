import json
import os

from src.event_processor.simple_authenticator import SimpleAuthenticator
from src.event_processor.payload_validator import PayloadValidator
from src.event_processor.database.db_connection_timeseries import DBConnectionTimeseries
from src.event_processor.logger.event_logger_new_relic import EventLoggerNewRelic
from src.event_processor.events.factory_event import FactoryEvent

def lambda_handler(event, context):
    
    try:
        client_auth_token = _get_auth_token(event)    
        event_payload = _get_event_payload(event)
    except Exception as e:
        print(f'Error initializing Lambda: {e}')
        return _get_response()
    
    try:
        preprocess_validation(client_auth_token, event_payload)
        process_new_event(event_payload)
    except Exception as e:
        print(f'Error processing event: {e}')

    return _get_response()


def process_new_event(event_payload: dict) -> None:
    
    database_name = os.getenv('DEVOPS_DB_NAME')
    table_name = os.getenv('DEVOPS_TABLE_NAME')

    db_connection = DBConnectionTimeseries(database_name, table_name)

    event_logger = EventLoggerNewRelic()

    factory_event = FactoryEvent(db_connection, event_logger)
    event = factory_event.create_event(event_payload)
    event.process()
    

def preprocess_validation(event_payload: dict, client_auth_token: str) -> None:

    expected_auth_token = os.getenv('SECRET_TOKEN', None)
    if SimpleAuthenticator(expected_auth_token).is_autherized(client_auth_token) == False:
        raise Exception('Unauthorized request')
    
    if PayloadValidator().is_payload_valid(event_payload) == False:
        raise Exception('Invalid payload')
    

def _get_auth_token(event) -> str:

    headers = event.get('headers', {})
    auth_token = headers.get('X-Secret-Token')
    return auth_token
    
def _get_event_payload(event) -> dict:
    payload = json.loads(event.get('body', '{}'))
    return payload
    
def _get_response():
     # Always return 200 success for security reasons
    response =  {
        'statusCode': 200,
        'body': json.dumps('Request processed successfully')
    }

    return response

import json
import os

from src.database.db_connection import DBConnection

class EventProcessor:

    EVENT_TYPES = ['push', 'deploy', 'test pass']
    MAX_PAYLOAD_SIZE = 2048

    def __init__(self, secret: str, db_connection: DBConnection) -> None:
        self.secret = secret
        self.db_connection = db_connection

    def process_event(self, event: dict, secret: str):
        
        if not self.is_autherized(secret):
            return
        
        if not self.is_payload_valid(event):
            return
        
        self.write_event_to_db(event)
        

        

    def is_autherized(self, token: str) -> bool:

        if token == self.secret:
            return True
        
        return False
    
    def is_payload_valid(self, payload: dict) -> bool:

        if len(payload) == 0:
            return False
        
        if len(payload) > self.MAX_PAYLOAD_SIZE:
            return False
        
        if payload is None:
            return False

        if 'repo_name' not in payload:
            return False

        if 'event' not in payload:
            return False
        
        if payload['event'] not in self.EVENT_TYPES:
            return False

        return True
    
    def write_event_to_db(self, payload: dict) -> None:

        self.db_connection.write_event_to_db(payload)

    

def lambda_handler(event, context):
    
    # Always return 200 success for security reasons
    RESPONSE =  {
        'statusCode': 200,
        'body': json.dumps('Request processed successfully')
    }

    headers = event.get('headers', {})
    auth_token = headers.get('X-Secret-Token')
    if auth_token is None:
        return RESPONSE

    try:
        payload = json.loads(event.get('body', '{}'))
    except json.JSONDecodeError:
        return RESPONSE

    secret_token = os.getenv('SECRET_TOKEN', None)

    event_processor = EventProcessor(secret_token)
    event_processor.process_event(payload, auth_token)

    return RESPONSE
    
from src.database.db_connection import DBConnection

class Event():

    def __init__(self, payload: dict, db_connection: DBConnection) -> None:
        self.payload = payload
        self.db_connection = db_connection

    def get_repo_name(self) -> str:
        return self.payload['repo_name']
    
    def get_event_type(self) -> str:
        return self.payload['event']
    
    def process(self) -> None:
        pass

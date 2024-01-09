import pandas as pd

from src.event_processor.database.db_connection import DBConnection

class Event():

    def __init__(self, payload: pd.DataFrame | dict, db_connection: DBConnection) -> None:
       
        if isinstance(payload, dict):
            self.payload = pd.DataFrame([payload])
        elif isinstance(payload, pd.DataFrame):
            self.payload = payload
        else:
            raise ValueError("Payload must be a dictionary or a pandas DataFrame")

        self.db_connection = db_connection


    def get_repo_name(self) -> str:
        return self.payload['Repo'].iloc[0]  
    
    def get_event_type(self) -> str:
        return self.payload['Event'].iloc[0]  
    
    def process(self) -> None:
        pass

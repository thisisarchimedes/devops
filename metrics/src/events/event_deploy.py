from src.events.event import Event

class EventDeploy(Event):

    def process(self) -> None:
        self.db_connection.write_event_to_db(self.payload)

    # Number of days in a week with at least one deploy
    def get_days_with_deploy(self) -> int:
        return self.db_connection.get_days_per_week_with_deploy(self.payload['repo_name'])
    

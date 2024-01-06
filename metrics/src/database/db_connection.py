from typing import List

class DBConnection():

    def __init__(self, database_name: str, table_name: str):
        self.database_name = database_name
        self.table_name = table_name

    def write_event_to_db(self, payload: dict):
        pass

    def get_all_repo_events(self, repo_name: str) -> list:
        pass

    def get_days_per_week_with_deploy(self, repos_name: List[str]) -> int:
        pass


import os
from dotenv import load_dotenv

from src.event_processor.config.config import Config

class ConfigLocal(Config):

    def __init__(self) -> None:
        load_dotenv()

    def get_expected_auth_token(self) -> str:
        return os.getenv('SECRET_TOKEN')

    def get_logger_api_key(self) -> str:
        return os.getenv('LOGGER_API_KEY')
    
    def get_db_name(self) -> str:
        return os.getenv('DEVOPS_DB_NAME')

    def get_db_table_name(self) -> str:
        return os.getenv('DEVOPS_TABLE_NAME')
    
    def get_deployment_freq_timeframe_days(self) -> int:
        return int(os.getenv('DEPLOYMENT_FREQ_TIMEFRAME_DAY'))
    


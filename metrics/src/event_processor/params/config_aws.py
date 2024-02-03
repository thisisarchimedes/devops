import os
import json
import boto3

from src.event_processor.params.config import Config


class ConfigAWS(Config):

    def __init__(self):
        self._initialize_param_store_client()
        self._initialize_secrets_manager_client()

    def get_expected_auth_token(self) -> str:
        secret = self._fetch_secret()
        return self._extract_value_from_secret(secret, 'DEVOPS_EVENTS_SECRET_TOKEN')

    def get_logger_api_key(self) -> str:
        secret = self._fetch_secret()
        return self._extract_value_from_secret(secret, 'LOGGER_API_KEY')

    def get_db_name(self) -> str:
        db_name = self._fetch_parameter_from_param_store('DEVOPS_DB_NAME')
        return db_name

    def get_db_table_name(self) -> str:  
        db_table_name = self._fetch_parameter_from_param_store('DEVOPS_TABLE_NAME')
        return db_table_name
        
    def get_deployment_freq_timeframe_days(self) -> int:
        days = self._fetch_parameter_from_param_store('DEPLOYMENT_FREQ_TIMEFRAME_DAY')
        return int(days)

    def get_secret_store_name(self) -> str:
        secret_store_name = self._fetch_parameter_from_param_store('SECRET_STORE_NAME')
        return secret_store_name

    def _initialize_secrets_manager_client(self):
        try:
            self.secrets_manager_client = boto3.client('secretsmanager')
            if self.secrets_manager_client is None:
                raise ValueError(
                    "Failed to initialize AWS Secrets Manager client.")
        except Exception as e:
            raise ValueError(
                f"Failed to initialize AWS Secrets Manager client: {str(e)}")

    def _fetch_secret(self):
        response = self.secrets_manager_client.get_secret_value(
            SecretId=self.get_secret_store_name())
        if 'SecretString' not in response:
            raise ValueError("Secret token not found in Secrets Manager.")

        return response['SecretString']
    def _extract_value_from_secret(self, secret_str, key):
        secret_dict = json.loads(secret_str)
        if key not in secret_dict:
            raise ValueError(f"{key} not found in the secret.")
        return secret_dict[key]
    
    def _initialize_param_store_client(self):
        try:
            self.ssm_client = boto3.client('ssm')
            if self.ssm_client is None:
                raise ValueError(
                    "Failed to initialize AWS SSM client.")
        except Exception as e:
            raise ValueError(
                f"Failed to initialize AWS SSM client: {str(e)}")
        
    def _fetch_parameter_from_param_store(self, param_name):
        try:
            response = self.ssm_client.get_parameter(
                Name=param_name, WithDecryption=True)
            return response['Parameter']['Value']
        except Exception as e:
            raise ValueError(f"Failed to fetch parameter {param_name}: {str(e)}")


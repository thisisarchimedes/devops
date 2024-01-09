import os
import argparse
import json
import requests

EVENT_TYPES = ['push', 'deploy', 'test pass']

class DevOpsEventReporter:

    def __init__(self, target_url: str, secret_token: str = None) -> None:
        self.target_url = target_url
        self.secret_token = secret_token

    def parse_cli_arguments(self) -> argparse.Namespace:
    
        parser = argparse.ArgumentParser()
        parser.add_argument('repo_name', help='The name of the repository')
        parser.add_argument('event', choices=EVENT_TYPES, help=f'The event to log (must be one of: {EVENT_TYPES}')
        parser.add_argument(
            '--metadata', help='Additional JSON metadata about the event', default="")
        
        return parser.parse_args()


    def prepare_record(self, repo_name, event, metadata) -> dict:
        record = {
            'Repo': repo_name,
            'Event': event,
            'Metadata': metadata
        }

        return record
    
    def post_event(self, record: dict) -> requests.Response:

        headers = {
            'X-Secret-Token': self.secret_token,
            'Content-Type': 'application/json'
        }

        response = requests.post(self.target_url, json=record, headers=headers)

        return response


def main():

    target_url = get_target_url()
    secret_token = get_secret_token()
    event_reporter = DevOpsEventReporter(target_url, secret_token)

    args = event_reporter.parse_cli_arguments()
    record = event_reporter.prepare_record(args.repo_name, args.event, args.metadata)
    response = event_reporter.post_event(record)

    if response.status_code == 200:
        print("Event logged successfully.")
    else:
        print("Event logging failed.")


def get_target_url() -> str:

    target_url = os.getenv('API_DEVOPS_EVENT_CATCHER', None)
    if target_url is None:
        raise ValueError("API_DEVOPS_EVENT_CATCHER environment variable is not set.")
    
    return target_url

def get_secret_token() -> str:
    
    secret_token = os.getenv('SECRET_TOKEN', None)
    if secret_token is None:
        raise ValueError("SECRET_TOKEN environment variable is not set.")
    
    return secret_token

if __name__ == "__main__":
    main()

import os
import argparse
import json
import requests

EVENT_TYPES = ['push', 'deploy', 'test pass']

class DevOpsEventReporter:

    def __init__(self, target_url: str):
        self.target_url = target_url

    def parse_cli_arguments(self) -> argparse.Namespace:
    
        parser = argparse.ArgumentParser()
        parser.add_argument('repo_name', help='The name of the repository')
        parser.add_argument('event', choices=EVENT_TYPES, help=f'The event to log (must be one of: {EVENT_TYPES}')
        parser.add_argument(
            '--metadata', help='Additional JSON metadata about the event', default="")
        
        return parser.parse_args()


    def prepare_record(self, repo_name, event, metadata) -> dict:
        record = {
            'repo_name': repo_name,
            'event': event,
            'metadata': metadata
        }

        return record
    
    def post_event(self, record: dict) -> requests.Response:
        response = requests.post(self.target_url, json=record)
        return response

    

def main():

    target_url = os.getenv('API_DEVOPS_EVENT_CATCHER', None)
    if target_url is None:
        raise ValueError("API_DEVOPS_EVENT_CATCHER environment variable is not set.")

    event_reporter = DevOpsEventReporter(target_url)

    args = event_reporter.parse_cli_arguments()
    record = event_reporter.prepare_record(args.repo_name, args.event, args.metadata)
    response = event_reporter.post_event(record)

    if response.status_code == 200:
        print("Event logged successfully.")
    else:
        print("Event logging failed.")


if __name__ == "__main__":
    main()

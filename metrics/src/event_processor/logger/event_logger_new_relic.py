import os
import dataclasses

from bson import json_util
import json

import requests
import pandas as pd
from dotenv import load_dotenv

from src.event_processor.logger.event_logger import EventLogItem, EventLogger


class EventLoggerNewRelic(EventLogger):

    def __init__(self) -> None:

        load_dotenv()

        self.new_relic_url = "https://log-api.newrelic.com/log/v1"
        self.api_key = os.getenv("NEW_RELIC_API_KEY")
        if not self.api_key:
            raise EnvironmentError("NEW_RELIC_API_KEY environment variable not set")
        

    def send_event_to_logger(self, event_log_item: pd.DataFrame) -> None:
              
        payload = self._get_event_payload_str(event_log_item)
        headers = self._get_request_headers()

        response = requests.post(self.new_relic_url, headers=headers, data=payload)
        if not response.ok:
            raise Exception(f"Failed to send event to New Relic: {response.text}")
        
        
    def _get_event_payload_str(self, event_log_item: EventLogItem) -> str:
        repo = event_log_item.event['Repo'].iloc[0]
        event_type = event_log_item.event['Event'].iloc[0]
        event_json = event_log_item.event.to_json(orient='records', lines=True)
        event_log_item = EventLogItem(
            environment='test',
            event=event_json,
            message=f'Repo: {repo} ; Event: {event_type}',
        )

        my_dict = dataclasses.asdict(event_log_item)
        json_event_log_item = json.dumps(my_dict, default=json_util.default)

        return json_event_log_item
        

    def _get_request_headers(self) -> dict:
        headers = {
            "Api-Key": self.api_key,
            "Content-Type": "application/json",
        }

        return headers

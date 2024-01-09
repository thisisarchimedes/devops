from dataclasses import dataclass
import pandas as pd

from src.event_processor.logger.event_logger import EventLogItem, EventLogger


class EventLoggerFake(EventLogger):

    logger_path = 'test/fake_db/logger.csv'

    def send_event_to_logger(self, event_log_item: EventLogItem) -> None:
        # Extract the DataFrame from the EventLogItem object
        event_df = event_log_item.event

        # Extract the necessary information from the DataFrame
        repo = event_df['Repo'].iloc[0]
        event_type = event_df['Event'].iloc[0]
        event_json = event_df.to_json(orient='records', lines=True)

        # Update the message of the event_log_item
        event_log_item.message = f'Repo: {repo} ; Event: {event_type}'

        # Save the event DataFrame to CSV
        event_df.to_csv(self.logger_path, mode='a+', header=False, index=False)

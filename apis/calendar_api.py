import requests
from datetime import datetime, timedelta
import logging
from config import CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CalendarAPI:
    def __init__(self, api_url: str, calendar_id: str, timezone: str):
        self.api_url = api_url
        self.calendar_id = calendar_id
        self.timezone = timezone


    def fetch_events_n_days_ahead(self, days_ahead: int = 7):
        """
        Retrieves calendar events for the specified number of days ahead.

        Args:
            days_ahead (int): Number of days in the future to retrieve events for.

        Returns:
            list: A list of calendar events.
        """
        # Convert days ahead into a time_max parameter
        time_max = datetime.now() + timedelta(days=days_ahead)
        time_max = time_max.replace(hour=0, minute=0, second=0, microsecond=0)
        time_max_str = time_max.isoformat()

        # Construct the request URL
        url = f"{self.api_url}/listEvents?calendarId={self.calendar_id}&orderBy=startTime&timeMax={time_max_str}Z&timeZone={self.timezone}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json().get('items', [])
        except requests.RequestException as e:
            logging.error(f"Error fetching calendar data: {e}")
            return []

    def extract_event_details(self, events_data: list) -> list:
        """
        Extracts and returns specific details from each event.
        Args:
            events_data (list): A list containing details for each event.
        Returns:
            list: A list of dictionaries with extracted event details.
        """
        extracted_data = []

        for event in events_data:
                task_info = {
                    "name": event.get("summary"),
                    "description": event.get("description"),
                    "duration": event.get("duration"),
                    "scheduled_start": event.get("start", {}).get("dateTime"),
                    "scheduled_end": event.get("end", {}).get("dateTime"),
                }
                extracted_data.append(task_info)

        return extracted_data

    def get_clean_event_data_n_days_ahead(self, n_days=7) -> list:
        """
        Fetches, processes, and returns clean and formatted task data.
        Returns:
            list: A list of dictionaries containing formatted task data.
        """
        raw_data = self.fetch_events_n_days_ahead(n_days)
        return sorted(self.extract_event_details(raw_data), key=lambda x: x.get('scheduled_start', {}))


if __name__ == '__main__':
    api = CalendarAPI(CONFIG["CALENDER_LINK"], CONFIG["CALENDER_ID"], CONFIG["CALENDAR_TIMEZONE"])
    events = api.get_clean_event_data_n_days_ahead(1)
    print(events)

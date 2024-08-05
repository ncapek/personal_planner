from apis.motion_api import MotionAPI
from apis.calendar_api import CalendarAPI
from config import CONFIG
from credentials_manager import CredentialsManager
import pytz


class ScheduleAPI:
    def __init__(self, motion_api: MotionAPI, calendar_api: CalendarAPI):
        """
        Initializes the ScheduleAPI with instances of MotionAPI and CalendarAPI.

        Args:
            motion_api (MotionAPI): An instance of the MotionAPI class.
            calendar_api (CalendarAPI): An instance of the CalendarAPI class.
        """
        self.motion_api = motion_api
        self.calendar_api = calendar_api

    def get_schedule(self, timezone: pytz.timezone, n_days: int = 7) -> dict:
        """
        Retrieves a combined list of tasks and events for the specified number of days ahead.

        Args:
            timezone (pytz.timezone): The timezone for the tasks and events.
            n_days (int): The number of days ahead to fetch tasks and events.

        Returns:
            dict: A dictionary containing lists of tasks and events.
        """
        tasks = self.motion_api.get_clean_task_data_n_days_ahead(timezone, n_days)
        events = self.calendar_api.get_clean_event_data_n_days_ahead(n_days)

        schedule = {
            'tasks': tasks,
            'events': events
        }

        return schedule

# Example usage
if __name__ == "__main__":
    credentials_manager = CredentialsManager()
    motion_api = MotionAPI(credentials_manager.get_credential("MOTION_API_KEY"))
    calendar_api = CalendarAPI(CONFIG["CALENDER_LINK"], CONFIG["CALENDER_ID"], CONFIG["CALENDAR_TIMEZONE"])
    schedule_api = ScheduleAPI(motion_api, calendar_api)

    schedule = schedule_api.get_schedule(CONFIG["TIMEZONE"], n_days=1)
    print(schedule)

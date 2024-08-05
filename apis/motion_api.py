"""
Motion Planner API Module.

This module provides a class-based interface for interacting with the Motion API. It includes functionalities for
retrieving tasks from a Motion planner and processing them into a structured and more readable format.
"""


import http.client
import json
import pytz
from datetime import datetime, timedelta
import logging
import requests
from config import CONFIG
from credentials_manager import CredentialsManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MotionAPI:
    def __init__(self, api_key: str):
        """
        Initializes the MotionAPI with the provided API key.
        Args:
            api_key (str): The API key for accessing the Motion API.
        """
        self.api_key = api_key
        self.base_url = "api.usemotion.com"

    def fetch_task_data(self) -> list:
        """
        Fetches task data from the Motion API, handling pagination with cursors.
        Returns:
            list: A list of task data dictionaries. Returns an empty list if an error occurs.
        """
        all_tasks = []
        cursor = None

        try:
            while True:
                conn = http.client.HTTPSConnection(self.base_url)
                headers = {'Accept': "application/json", 'X-API-Key': self.api_key}

                path = "/v1/tasks"
                if cursor:
                    path += f"?cursor={cursor}"

                conn.request("GET", path, headers=headers)
                res = conn.getresponse()
                data = res.read()
                response = json.loads(data.decode("utf-8"))

                all_tasks.extend(response.get("tasks", []))
                cursor = response.get("meta", {}).get("nextCursor")

                if not cursor:
                    break

            return all_tasks

        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON response: {e}")
        except Exception as e:
            logger.error(f"Error fetching task data: {e}")

        return []

    def fetch_specific_task_data(self, task_id: str) -> dict:
        """
        Fetches data for a specific task from the Motion API.

        Args:
            task_id (str): The unique identifier of the task to retrieve.

        Returns:
            dict: The retrieved task data. Returns an empty dictionary if an error occurs.
        """
        url = f"https://{self.base_url}/v1/tasks/{task_id}"
        headers = {
            'Accept': "application/json",
            'X-API-Key': self.api_key
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching task data: {e}")

        return {}

    def get_task_data_n_days_ahead(self, timezone: pytz.timezone, n_days: int = 7) -> list:
        """
        Fetches task data from the Motion API for the specified number of days ahead.

        Args:
            timezone (pytz.timezone): The timezone in which the dates should be considered.
            n_days (int): The number of days ahead to fetch tasks for.

        Returns:
            list: A list of task data dictionaries for the relevant days.
        """
        all_tasks = self.fetch_task_data()
        relevant_tasks = []
        max_date = datetime.now(timezone) + timedelta(days=n_days, hours=0, minutes=0, seconds=0)
        max_date = max_date.replace(hour=0, minute=0, second=0)

        for task in all_tasks:
            scheduled_start = task.get("scheduledStart")
            if scheduled_start:
                today = datetime.now(timezone).replace(hour=0, minute=0, second=0)
                task_date = self._parse_date(scheduled_start, timezone)
                if today <= task_date <= max_date:
                    relevant_tasks.append(task)

        return relevant_tasks

    @staticmethod
    def _parse_date(date_str: str, timezone: pytz.timezone) -> datetime.date:
        """
        Parses an ISO formatted date string to a timezone-aware datetime object.

        Args:
            date_str (str): The ISO formatted date string.
            timezone (pytz.timezone): The timezone to apply.

        Returns:
            datetime.date: The parsed date.
        """
        return datetime.fromisoformat(date_str.replace('Z', '+00:00')).astimezone(timezone)


    def extract_task_details(self, tasks_data: list) -> list:
        """
        Extracts and returns specific details from each task.
        Args:
            task_data (list): A list containing details for each task.
        Returns:
            list: A list of dictionaries with extracted task details.
        """
        extracted_data = []

        for task in tasks_data:
                task_info = {
                    "name": task.get("name"),
                    "description": task.get("description"),
                    "duration": task.get("duration"),
                    "scheduled_start": task.get("scheduledStart"),
                    "due_date": task.get("dueDate"),
                    "type": task.get("labels", [{}])[0].get('name') if task.get("labels") else ""
                }
                extracted_data.append(task_info)

        return extracted_data

    def get_clean_task_data_n_days_ahead(self, timezone, n_days=7) -> list:
        """
        Fetches, processes, and returns clean and formatted task data.
        Returns:
            list: A list of dictionaries containing formatted task data.
        """
        raw_data = self.get_task_data_n_days_ahead(timezone, n_days)
        return sorted(self.extract_task_details(raw_data), key=lambda x: x['scheduled_start'])


if __name__ == "__main__":
    credentials_manager = CredentialsManager()
    motion_api = MotionAPI(credentials_manager.get_credential("MOTION_API_KEY"))
    clean_task_data = motion_api.get_clean_task_data_n_days_ahead(CONFIG["TIMEZONE"], CONFIG["N_DAYS_AHEAD"])
    print(clean_task_data)
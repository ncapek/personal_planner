"""
Motion Planner API Module.

This module provides a class-based interface for interacting with the Motion API. It includes functionalities for
retrieving tasks from a Motion planner and processing them into a structured and more readable format.

Classes:
    MotionAPI: A class to interact with the Motion API for planner tasks.

Example:
    motion_api = MotionAPI(MOTION_API_KEY)
    tasks = motion_api.get_clean_task_data()

Note:
    Requires a Motion API key for access.
"""


import http.client
import json
import logging
from config import MOTION_API_KEY

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

    def fetch_task_data(self) -> dict:
        """
        Fetches task data from the Motion API.

        Returns:
            dict: JSON response as a dictionary. Returns an empty dict if an error occurs.
        """
        try:
            conn = http.client.HTTPSConnection(self.base_url)
            headers = {'Accept': "application/json", 'X-API-Key': self.api_key}
            conn.request("GET", "/v1/tasks", headers=headers)
            res = conn.getresponse()
            data = res.read()
            return json.loads(data.decode("utf-8"))
        except json.JSONDecodeError as e:
            logger.error("Error decoding JSON response: {}".format(e))
            return {}
        except Exception as e:
            logger.error("Error fetching task data: {}".format(e))
            return {}

    def extract_task_details(self, task_data: dict) -> list:
        """
        Extracts and returns specific details from each task.

        Args:
            task_data (dict): The JSON response containing task details.

        Returns:
            list: A list of dictionaries with extracted task details.
        """

        tasks = task_data.get("tasks", [])
        extracted_data = []

        for task in tasks:
            task_type = ""
            if task.get("labels") and isinstance(task["labels"], list):
                task_type = task["labels"][0]['name']

            # Add task information to the extracted data
            task_info = {
                "name": task.get("name"),
                "description": task.get("description"),
                "duration": task.get("duration"),
                "due_date": task.get("dueDate"),
                "type": task_type
            }
            extracted_data.append(task_info)

        return extracted_data

    def get_clean_task_data(self) -> list:
        """
        Fetches, processes, and returns clean and formatted task data.

        Combines the process of fetching task data and formatting it into a more readable and useful format.

        Returns:
            list: A list of dictionaries containing formatted task data.
        """
        raw_data = self.fetch_task_data()
        if not raw_data:
            return []

        return self.extract_task_details(raw_data)

if __name__ == "__main__":
    motion_api = MotionAPI(MOTION_API_KEY)
    clean_task_data = motion_api.get_clean_task_data()
    print(clean_task_data)
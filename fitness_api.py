"""
Fitness Data Module.

This module provides a class-based interface to fetch and process fitness-related data. It encapsulates functionalities
to retrieve various health metrics and offers clean, processed data suitable for further analysis or display.

Classes:
    FitnessAPI: A class to interact with a specified fitness data API.

Example:
    fitness_api = FitnessAPI(NOCODE_API_LINK)
    fitness_api.get_clean_fitness_data()

Note:
    Requires an API endpoint to fetch fitness data.
"""

import requests
import logging
from personal_planner.config import NOCODE_API_LINK

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FitnessAPI:
    def __init__(self, api_url: str):
        """
        Initializes the FitnessAPI with the provided API URL.

        Args:
            api_url (str): The API endpoint URL for fetching fitness data.
        """
        self.api_url = api_url

    def fetch_health_data(self, params: dict = {}) -> dict:
        """
        Fetches health data from the API.

        Args:
            params (dict): Parameters for the GET request.

        Returns:
            dict: JSON response as a dictionary. Returns an empty dict if an error occurs.
        """
        try:
            response = requests.get(url=self.api_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error: {e}")
        return {}

    def extract_relevant_data(self, result: dict) -> dict:
        """
        Extracts relevant key-value pairs from the JSON response.

        Args:
            result (dict): The JSON response as a dictionary.

        Returns:
            dict: Dictionary with extracted key-value pairs.
        """
        extracted_data = {}
        keys_of_interest = ['steps_count', 'weight', 'active_minutes', 'calories_expended', 'heart_minutes', 'sleep_segment', 'activity_summary']
        for key in keys_of_interest:
            if key in result and len(result[key]) == 1:
                extracted_data[key] = result[key][0]['value']
        return extracted_data

    def get_clean_fitness_data(self, params: dict = {}) -> dict:
        """
        Fetches, processes, and returns clean and formatted fitness data.

        This method combines the process of fetching fitness data and formatting it into a more readable and useful format.

        Args:
            params (dict): Parameters for the GET request to the fitness data API.

        Returns:
            dict: A dictionary containing formatted fitness data. Returns an empty dict if fetching fails or data is incomplete.
        """
        raw_data = self.fetch_health_data(params)
        if not raw_data:
            return {}

        return self.extract_relevant_data(raw_data)

if __name__ == "__main__":
    fitness_api = FitnessAPI(NOCODE_API_LINK)
    result = fitness_api.get_clean_fitness_data()
    print(result)
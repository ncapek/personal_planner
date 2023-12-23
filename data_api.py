"""
Module: Combined API Integration

This module contains the CombinedAPI class that integrates multiple individual APIs
(WeatherAPI, FitnessAPI, and MotionAPI) to fetch and process a variety of personal data.
It serves as a unified interface to aggregate data from weather forecasts, fitness tracking,
and personal planning tasks. The class aims to simplify the process of gathering and
synthesizing diverse data sources for comprehensive personal reports.

The CombinedAPI class requires instances of the specific APIs as input and provides methods
to fetch and combine their data. It allows fetching weather data based on geographical
coordinates and integrates this with fitness and planner data to create a consolidated overview.

Example usage demonstrates how to initialize the CombinedAPI with individual API instances
and retrieve combined data for specified latitude and longitude.

Classes:
    CombinedAPI: Facilitates the integration and processing of data from WeatherAPI, FitnessAPI,
                 and MotionAPI into a single, combined output.

Example:
    combined_api = CombinedAPI(weather_api, fitness_api, motion_api)
    combined_data = combined_api.get_combined_data(latitude, longitude, timezone)
    print(combined_data)
"""


import logging
from weather_api import WeatherAPI
from fitness_api import FitnessAPI
from motion_api import MotionAPI
from config import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CombinedAPI:
    def __init__(self, weather_api: WeatherAPI, fitness_api: FitnessAPI, motion_api: MotionAPI):
        """
        Initializes the CombinedAPI with instances of WeatherAPI, FitnessAPI, and MotionAPI.

        Args:
            weather_api (WeatherAPI): An instance of the WeatherAPI class.
            fitness_api (FitnessAPI): An instance of the FitnessAPI class.
            motion_api (MotionAPI): An instance of the MotionAPI class.
        """
        self.weather_api = weather_api
        self.fitness_api = fitness_api
        self.motion_api = motion_api

    def get_combined_data(self, latitude: float, longitude: float, timezone: str) -> dict:
        """
        Fetches and processes data from Weather, Fitness, and Motion APIs.

        Args:
            latitude (float): The latitude for the weather data.
            longitude (float): The longitude for the weather data.

        Returns:
            dict: A dictionary containing combined data from all three APIs.
        """
        combined_data = {}

        # Fetch and process weather data using the provided latitude and longitude
        weather_data = self.weather_api.get_clean_weather_data(latitude, longitude, timezone)
        combined_data['weather'] = weather_data

        # Fetch and process fitness data
        fitness_data = self.fitness_api.get_clean_fitness_data()
        combined_data['fitness'] = fitness_data

        # Fetch and process motion planner data
        motion_data = self.motion_api.get_clean_task_data()
        combined_data['planner'] = motion_data

        return combined_data

# Example usage
if __name__ == "__main__":
    weather_api = WeatherAPI(OPENWEATHER_API_KEY)
    fitness_api = FitnessAPI(NOCODE_API_LINK)
    motion_api = MotionAPI(MOTION_API_KEY)

    combined_api = CombinedAPI(weather_api, fitness_api, motion_api)
    data = combined_api.get_combined_data(LATITUDE, LONGITUDE, TIMEZONE)
    print(data)

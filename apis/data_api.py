"""
Module: Combined API Integration

This module contains the CombinedDataAPI class that integrates multiple individual APIs
(WeatherAPI, FitnessAPI, and MotionAPI) to fetch and process a variety of personal data.
It serves as a unified interface to aggregate data from weather forecasts, fitness tracking,
and personal planning tasks. The class aims to simplify the process of gathering and
synthesizing diverse data sources for comprehensive personal reports.

The CombinedDataAPI class requires instances of the specific APIs as input and provides methods
to fetch and combine their data. It allows fetching weather data based on geographical
coordinates and integrates this with fitness and planner data to create a consolidated overview.

Example usage demonstrates how to initialize the CombinedDataAPI with individual API instances
and retrieve combined data for specified latitude and longitude.

Classes:
    CombinedDataAPI: Facilitates the integration and processing of data from WeatherAPI, FitnessAPI,
                 and MotionAPI into a single, combined output.

Example:
    schedule_api = CombinedDataAPI(weather_api, fitness_api, schedule_api)
    combined_data = schedule_api.get_combined_data(latitude, longitude, timezone)
    print(combined_data)
"""

import logging
import pytz
from apis.weather_api import WeatherAPI
from apis.fitness_api import FitnessAPI
from apis.motion_api import MotionAPI
from apis.calendar_api import CalendarAPI
from apis.schedule_api import ScheduleAPI
from config import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CombinedDataAPI:
    def __init__(self, weather_api: WeatherAPI, fitness_api: FitnessAPI, schedule_api: ScheduleAPI):
        """
        Initializes the CombinedDataAPI with instances of WeatherAPI, FitnessAPI, and MotionAPI.

        Args:
            weather_api (WeatherAPI): An instance of the WeatherAPI class.
            fitness_api (FitnessAPI): An instance of the FitnessAPI class.
            schedule_api (ScheduleAPI): An instance of the ScheduleAPI class.
        """
        self.weather_api = weather_api
        self.fitness_api = fitness_api
        self.schedule_api = schedule_api

    def get_combined_data(self, latitude: float, longitude: float, timezone, n_days_ahead: int = 1) -> dict:
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
        fitness_data = self.fitness_api.get_clean_data()
        combined_data['fitness'] = fitness_data

        # Fetch and process motion planner data
        schedule_data = self.schedule_api.get_schedule(timezone, n_days_ahead)
        combined_data['schedule'] = schedule_data

        return combined_data


if __name__ == "__main__":
    APIS = {
        'weather_api': WeatherAPI(OPENWEATHER_API_KEY),
        'fitness_api': FitnessAPI(**GARMIN),
        'schedule_api': ScheduleAPI(MotionAPI(MOTION_API_KEY),
                                    CalendarAPI(CALENDER_LINK, CALENDER_ID, CALENDAR_TIMEZONE)),
    }
    data_api = CombinedDataAPI(**APIS)
    data = data_api.get_combined_data(LATITUDE, LONGITUDE, TIMEZONE, 1)
    print(data)

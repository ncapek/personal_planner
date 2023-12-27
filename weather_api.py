"""
Weather API Module.

This module provides access to weather data via the OpenWeatherMap One Call API. It includes the WeatherAPI class,
which offers methods to fetch detailed weather data for a specific latitude and longitude. Features include fetching
raw weather data, extracting and formatting relevant data points for easier consumption, and utility functions for
time conversion. The module is designed to be easy to use while providing robust error handling and logging capabilities.

Classes:
    WeatherAPI: A class to interact with and process data from the OpenWeatherMap API.

Example:
    weather_api = WeatherAPI(api_key)
    weather_data = weather_api.get_clean_weather_data(latitude, longitude, timezone)

Note:
    An API key from OpenWeatherMap is required to use this module.
"""

import requests
from datetime import datetime
import pytz
import logging
from config import OPENWEATHER_API_KEY, LATITUDE, LONGITUDE, TIMEZONE
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeatherAPI:
    """
    A class to interact with the OpenWeatherMap One Call API.

    This class provides methods to fetch weather data for a given location
    specified by latitude and longitude, and to process this data into a
    more user-friendly format.

    Attributes:
        api_key (str): The API key for accessing the OpenWeatherMap API.
        base_url (str): The base URL for the OpenWeatherMap One Call API.
    """

    def __init__(self, api_key: str):
        """
        Initializes the WeatherAPI with the provided API key.

        Args:
            api_key (str): The API key for accessing the OpenWeatherMap API.
        """
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/3.0/onecall"

    def get_weather_data(self, lat: float, lon: float) -> dict:
        """
        Fetches weather data from the OpenWeatherMap API for the specified latitude and longitude.

        This method sends a request to the OpenWeatherMap One Call API and returns the JSON response.

        Args:
            lat (float): The latitude of the location.
            lon (float): The longitude of the location.

        Returns:
            dict: A dictionary containing the weather data from the API. Returns an empty dict if an error occurs.
        """
        try:
            response = requests.get(self.base_url, params={
                'lat': lat, 'lon': lon, 'appid': self.api_key, 'units': 'metric'
            })
            response.raise_for_status()  # Raises an HTTPError for 4xx/5xx responses
            return response.json()
        except HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
        except ConnectionError:
            logger.error("Connection error occurred")
        except Timeout:
            logger.error("Request timed out")
        except RequestException as e:
            logger.error(f"Error fetching weather data: {e}")
        return {}

    def get_clean_weather_data(self, lat: float, lon: float, timezone_str: str) -> dict:
        """
        Fetches, processes, and returns clean and formatted weather data for a given location.

        This method combines the process of fetching weather data and formatting it into a more readable and useful format.

        Args:
            lat (float): The latitude of the location.
            lon (float): The longitude of the location.
            timezone_str (str): The timezone string for time conversion.

        Returns:
            dict: A dictionary containing formatted weather data.
        """
        raw_data = self.get_weather_data(lat, lon)
        if not raw_data:
            return {}

        return self.extract_relevant_data(raw_data, timezone_str)

    @staticmethod
    def convert_unix_to_readable(unix_timestamp: int, timezone_str: str) -> str:
        """
        Converts a UNIX timestamp to a human-readable date and time string in the specified timezone.

        Args:
            unix_timestamp (int): The UNIX timestamp to convert.
            timezone_str (str): The timezone string for the conversion.

        Returns:
            str: A human-readable date and time string. Returns 'Invalid time' if an error occurs.
        """
        try:
            timezone = pytz.timezone(timezone_str)
            date_time_local = datetime.fromtimestamp(unix_timestamp, timezone)
            return date_time_local.strftime("%Y-%m-%d %H:%M:%S %Z")
        except Exception as e:
            logger.error(f"Error converting timestamp: {e}")
            return "Invalid time"

    def extract_relevant_data(self, api_response: dict, timezone_str: str) -> dict:
        """
        Extracts and formats relevant weather data from the API response.

        This method processes the raw API response to extract useful information like current weather,
        daily forecast, and weather alerts, and formats them into a more readable structure.

        Args:
            api_response (dict): The raw API response to process.
            timezone_str (str): The timezone string for time conversion.

        Returns:
            dict: A dictionary containing the formatted weather data.
        """
        if 'current' not in api_response or 'daily' not in api_response or not isinstance(api_response.get('daily', []),
                                                                                          list):
            logger.warning("Invalid or insufficient API response")
            return {}

        formatted_data = {
            'current_weather': self.format_current_weather(api_response['current'], timezone_str),
            'today_forecast': self.format_daily_forecast(api_response['daily'][0])
        }

        if 'alerts' in api_response:
            formatted_data['alerts'] = self.format_alerts(api_response['alerts'], timezone_str)
        return formatted_data

    def format_current_weather(self, current_weather: dict, timezone_str: str) -> dict:
        """
        Formats the current weather data into a readable format.

        Args:
            current_weather (dict): The 'current' section of the API response.
            timezone_str (str): The timezone string for time conversion of sunrise and sunset.

        Returns:
            dict: A dictionary containing formatted current weather information.
        """
        return {
            'temperature': f"{current_weather['temp']}°C",
            'description': current_weather['weather'][0]['description'],
            'sunrise': self.convert_unix_to_readable(current_weather['sunrise'], timezone_str),
            'sunset': self.convert_unix_to_readable(current_weather['sunset'], timezone_str),
            'wind_speed': f"{current_weather['wind_speed']} m/s",
            'humidity': f"{current_weather['humidity']}%"
        }

    def format_daily_forecast(self, daily_forecast: dict) -> dict:
        """
        Formats the daily forecast data into a readable format.

        Args:
            daily_forecast (dict): The 'daily' section (first entry) of the API response.

        Returns:
            dict: A dictionary containing formatted information about today's weather forecast.
        """
        return {
            'max_temp': f"{daily_forecast['temp']['max']}°C",
            'min_temp': f"{daily_forecast['temp']['min']}°C",
            'conditions': daily_forecast['weather'][0]['description']
        }

    def format_alerts(self, alerts: list, timezone_str: str) -> list:
        """
        Formats weather alerts into a readable format.

        Args:
            alerts (list): The 'alerts' section of the API response.
            timezone_str (str): The timezone string for time conversion of alert start and end times.

        Returns:
            list: A list of dictionaries, each containing information about a weather alert.
        """
        formatted_alerts = []
        for alert in alerts:
            formatted_alert = {
                'title': alert.get('event'),
                'description': alert.get('description'),
                'start': self.convert_unix_to_readable(alert['start'], timezone_str) if 'start' in alert else None,
                'end': self.convert_unix_to_readable(alert['end'], timezone_str) if 'end' in alert else None
            }
            formatted_alerts.append(formatted_alert)
        return formatted_alerts


if __name__ == '__main__':
    weather_api = WeatherAPI(OPENWEATHER_API_KEY)
    weather_info = weather_api.get_clean_weather_data(LATITUDE, LONGITUDE, TIMEZONE)
    print(weather_info)
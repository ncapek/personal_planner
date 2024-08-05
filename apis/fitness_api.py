"""
Fitness Data Module for Garmin Connect.

This module provides a class-based interface to fetch and process fitness data from Garmin Connect. It encapsulates
functionalities to retrieve various health metrics and offers clean, processed data suitable for further analysis or display.
"""

import garminconnect
from datetime import date, timedelta
from credentials_manager import CredentialsManager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FitnessAPI:
    def __init__(self, email: str, password: str):
        """
        Initializes the FitnessAPI with Garmin Connect credentials.

        Args:
            email (str): The user's Garmin Connect email.
            password (str): The user's Garmin Connect password.
        """
        self.client = garminconnect.Garmin(email, password)
        self.login()

    def login(self):
        """
        Logs into the Garmin Connect API.
        """
        try:
            self.client.login()
        except Exception as e:
            logger.error(f"Login error: {e}")

    def fetch_user_data_by_date(self, date: str) -> dict:
        """
        Fetches health data for a specific date from Garmin Connect.

        Args:
            date (str): The date for which to fetch data in 'YYYY-MM-DD' format.

        Returns:
            dict: Health data for the specified date. Returns an empty dict if an error occurs.
        """
        try:
            return self.client.get_user_summary(date)
        except Exception as e:
            logger.error(f"Error fetching health data: {e}")
            return {}

    def get_clean_data_by_date(self, date: str) -> dict:
        """
        Extracts relevant health and fitness data from the Garmin Connect API response.

        Args:
            response (dict): The JSON response from the Garmin Connect API.

        Returns:
            dict: A dictionary containing the extracted key-value pairs.
        """
        response = self.fetch_user_data_by_date(date)
        extracted_data = {
            'total_steps': response.get('totalSteps'),
            'daily_steps_goals': response.get('dailyStepGoal'),
            'total_distance_kilometers': round(response.get('totalDistanceMeters') / 1000, 2) if response.get('totalDistanceMeters') else None,
            'active_kilocalories': response.get('activeKilocalories'),
            'resting_heart_rate': response.get('restingHeartRate'),
            'min_heart_rate': response.get('minHeartRate'),
            'max_heart_rate': response.get('maxHeartRate'),
            'seven_day_average_resting_heart_rate': response.get('lastSevenDaysAvgRestingHeartRate'),
            'average_stress_level': response.get('averageStressLevel'),
            'max_stress_level': response.get('maxStressLevel'),
            'sleep_duration_hours': round(response.get('sleepingSeconds') / 3600, 2) if response.get('sleepingSeconds') else None,
            'floors_ascended': response.get('floorsAscended'),
            # 'floors_descended': response.get('floorsDescended'),
            # 'body_battery_lowest': response.get('bodyBatteryLowestValue'),
            # 'body_battery_highest': response.get('bodyBatteryHighestValue'),
            'sedentary_minutes': round(response.get('sedentarySeconds') / 60, 2) if response.get('sedentarySeconds') else None,
            'respiration_rate': {
                'average': response.get('avgWakingRespirationValue'),
                'highest': response.get('highestRespirationValue'),
                'lowest': response.get('lowestRespirationValue'),
                'latest': response.get('latestRespirationValue')
            },
            'stress_data': {
                'stress_qualifier': response.get('stressQualifier'),
                'total_stress_percentage': response.get('stressPercentage'),
                'proportion_of_total_stress': {
                    'rest_stress': response.get('restStressPercentage'),
                    'activity_stress': response.get('activityStressPercentage'),
                    'uncategorized_stress': response.get('uncategorizedStressPercentage'),
                    'low_stress': response.get('lowStressPercentage'),
                    'medium_stress': response.get('mediumStressPercentage'),
                    'high_stress': response.get('highStressPercentage')
                    }
            }
            # Add any other relevant metrics you want to track
        }

        return extracted_data

    def get_clean_data(self) -> dict:
        """
        Fetches, processes, and returns clean and formatted fitness data for the previous day.

        Returns:
            dict: A dictionary containing formatted fitness data for yesterday.
        """
        data_dict = {}
        for i in range(7):
            data_date = (date.today() - timedelta(days=i)).isoformat()
            data_dict[data_date] = self.get_clean_data_by_date(data_date)
        return data_dict

if __name__ == "__main__":
    credentials_manager = CredentialsManager()
    fitness_api = FitnessAPI(credentials_manager.get_credential("GARMIN_EMAIL"), credentials_manager.get_credential("GARMIN_PASSWORD"))
    result = fitness_api.get_clean_data()
    print(result)

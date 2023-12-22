import requests
from config import NOCODE_API_LINK

def fetch_health_data(url: str, params: dict) -> dict:
    """
    Fetch health data from the given URL.

    :param url: API endpoint URL.
    :param params: Parameters for the GET request.
    :return: JSON response as a dictionary.
    """
    try:
        response = requests.get(url=url, params=params)
        response.raise_for_status()  # Raises HTTPError for bad requests
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def extract_relevant_data(result: dict) -> dict:
    """
    Extracts relevant key-value pairs from the JSON response.

    :param result: The JSON response as a dictionary.
    :return: Dictionary with extracted key-value pairs.
    """
    extracted_data = {}
    for key in ['steps_count', 'weight', 'active_minutes', 'calories_expended', 'heart_minutes', 'sleep_segment', 'activity_summary']:
        if key in result:
            if len(result[key]) == 1:
                extracted_data[key] = result[key][0]['value']
    return extracted_data

if __name__ == "__main__":
    # Example usage
    url = NOCODE_API_LINK
    params = {}
    result = fetch_health_data(url, params)

    if result:
        relevant_data = extract_relevant_data(result)
        print(relevant_data)

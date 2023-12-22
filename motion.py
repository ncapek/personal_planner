import http.client
import json
from config import MOTION_API_KEY

def extract_task_details(task_data: dict) -> list:
    """
    Extracts and returns specific details from each task.

    :param task_data: The JSON response containing task details.
    :return: A list of dictionaries with extracted task details.
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

# API request
conn = http.client.HTTPSConnection("api.usemotion.com")
headers = {
    'Accept': "application/json",
    'X-API-Key': MOTION_API_KEY
}
conn.request("GET", "/v1/tasks", headers=headers)

res = conn.getresponse()
data = res.read()

# Parse the response and extract task details
try:
    json_data = json.loads(data.decode("utf-8"))
    extracted_tasks = extract_task_details(json_data)
    print(extracted_tasks)
except json.JSONDecodeError:
    print("Error decoding JSON response")

# Optional: Print the raw JSON response
# print(data.decode("utf-8"))

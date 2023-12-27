"""
This module orchestrates a daily personal briefing by gathering data from various sources,
processing it through a language model, and then sending the output via email.

It integrates different APIs for weather, fitness, and motion data, creating a comprehensive
snapshot of the user's daily activities and environmental conditions. This data, along with
personal context, is fed into a language model (such as OpenAI's GPT) to generate insights
and suggestions tailored to the user's profile. The module utilizes the langchain package to
efficiently construct prompts for the language model. Finally, the insights are delivered to
the user's email, leveraging the SendGrid API for email dispatch.

This module is part of a broader application aimed at enhancing personal productivity and
self-awareness through data-driven insights. It serves as an automated, intelligent assistant
providing daily updates and advice.

Usage:
    The module is executed as a standalone script. It requires proper configuration of API keys
    and user-specific details in the config file. Once configured, the script can be scheduled
    to run daily, providing a consistent and automated personal briefing.

Note:
    Ensure all required API keys and configurations are securely set in the config module
    before running this script.
"""

from data_api import CombinedAPI
from motion_api import MotionAPI
from weather_api import WeatherAPI
from fitness_api import FitnessAPI
from language_model_api import OpenAIGPTAPI
from sendgrid_api import send_email
from langchain.prompts import PromptTemplate
from config import (OPENWEATHER_API_KEY, NOCODE_API_LINK, MOTION_API_KEY,
                    OPENAI_API_KEY, FROM_EMAIL, TO_EMAIL, SUBJECT,
                    LATITUDE, LONGITUDE, TIMEZONE, COMMAND, CONTEXT)
import logging

# Configure logging for better debugging and tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_prompt(command: str, context: str, personal_data: str) -> str:
    """
    Generates a prompt for the language model using provided command, context, and personal data.

    Args:
        command (str): The command or question for the language model.
        context (str): Contextual information about the user.
        personal_data (str): Personal data to be included in the prompt.

    Returns:
        str: A formatted prompt for the language model.
    """
    prompt_template = PromptTemplate.from_template(
        "{command}\n\nContext: <{context}>\n\nPersonal data: <{personal_data}>"
    )
    return prompt_template.format(command=command, context=context, personal_data=personal_data)

def gather_data() -> dict:
    """
    Gathers combined data from various APIs including weather, fitness, and motion.

    Returns:
        str: Combined data in a structured format.
    """
    try:
        weather_api = WeatherAPI(OPENWEATHER_API_KEY)
        fitness_api = FitnessAPI(NOCODE_API_LINK)
        motion_api = MotionAPI(MOTION_API_KEY)
        combined_api = CombinedAPI(weather_api, fitness_api, motion_api)
        return combined_api.get_combined_data(LATITUDE, LONGITUDE, TIMEZONE)
    except Exception as e:
        logger.error("Error gathering data: %s", e)
        raise

def get_language_model_response(prompt: str) -> str:
    """
    Queries the OpenAI language model with the provided prompt.

    Args:
        prompt (str): The prompt to query the language model with.

    Returns:
        str: The response from the language model.
    """
    try:
        openai_api = OpenAIGPTAPI(OPENAI_API_KEY)
        response = openai_api.query(prompt)
        return response.choices[0].message.content
    except Exception as e:
        logger.error("Error querying the language model: %s", e)
        raise

def main():
    """
    Main function to execute the workflow of gathering data, creating a prompt,
    getting a response from the language model, and sending an email.
    """
    try:
        data = gather_data()
        prompt = create_prompt(COMMAND, CONTEXT, data)
        response = get_language_model_response(prompt)
        response = response + f'\n\n\n\ndata: {data}'
        send_email(from_email=FROM_EMAIL, to_email=TO_EMAIL, subject=SUBJECT, html_content=response)
        logger.info("Morning briefing successfully sent by email.")
    except Exception as e:
        logger.error("An error occurred in the main workflow: %s", e)

if __name__ == '__main__':
    main()

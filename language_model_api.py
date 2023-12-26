"""
This module provides an abstract base class and its concrete implementations to interact with various language models.
It includes an implementation for OpenAI's GPT model and a hypothetical local language model. The module allows for
querying these models with a given input and obtaining their responses, facilitating easy integration and usage of
different language models in a unified way.
"""

import openai
from abc import ABC, abstractmethod
from data_api import *
from weather_api import *
from motion_api import *
from fitness_api import *
from config import OPENAI_API_KEY

class LanguageModelAPI(ABC):
    @abstractmethod
    def query(self, input_data: str) -> str:
        """
        Sends a query to the language model and returns the response.
        Args:
            input_data (str): The input data or prompt to send to the model.
        Returns:
            str: The response from the language model.
        """
        pass

class OpenAIGPTAPI(LanguageModelAPI):
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """
        Initializes the OpenAI GPT API with the provided API key.
        Args:
            api_key (str): The API key for OpenAI.
        """
        openai.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model  # Default model, can be changed if needed

    def query(self, prompt: str, temperature: float = 0) -> str:
        """
        Sends a query to the OpenAI GPT model using the Chat Completion endpoint.
        Args:
            prompt (str): The user's input prompt.
            temperature (float): The degree of randomness in the model's output.
        Returns:
            str: The response from the GPT model.
        """
        messages = [{"role": "user", "content": prompt}]
        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo"
        )
        return chat_completion

class LocalLLMAPI(LanguageModelAPI):
    def __init__(self, model_path: str):
        """
        Initializes the local LLM API with the provided model path.
        Args:
            model_path (str): The path to the local language model.
        """
        self.model = load_local_model(model_path)  # Hypothetical function to load a local model

    def query(self, input_data: str) -> str:
        """
        Sends a query to the local language model and returns the response.
        Args:
            input_data (str): The input data or prompt to send to the model.
        Returns:
            str: The response from the local model.
        """
        response = self.model.generate_response(input_data)
        return response

def use_language_model(api: LanguageModelAPI, input_text: str) -> str:
    """
    Utilizes the provided language model API to send a query and get a response.
    Args:
        api (LanguageModelAPI): The language model API to use.
        input_text (str): The text input for the model.
    Returns:
        str: The response from the model.
    """
    return api.query(input_text)

if __name__ == "__main__":
    # Setup APIs
    openai_api = OpenAIGPTAPI(OPENAI_API_KEY)
    weather_api = WeatherAPI(OPENWEATHER_API_KEY)
    fitness_api = FitnessAPI(NOCODE_API_LINK)
    motion_api = MotionAPI(MOTION_API_KEY)
    combined_api = CombinedAPI(weather_api, fitness_api, motion_api)
    # Gather personal data
    data = combined_api.get_combined_data(LATITUDE, LONGITUDE, TIMEZONE)

    template = f"Construct a briefing for my day, based on the following data\n\npersonal_data: {data}"
    print(template)
    response = openai_api.query(template)
    print(response.choices[0].message.content)
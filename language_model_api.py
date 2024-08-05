import openai
from abc import ABC, abstractmethod
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
    def __init__(self, api_key: str):
        """
        Initializes the OpenAI GPT API with the provided API key.
        """
        openai.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)
        self.model = "gpt-3.5-turbo"  # Default model, can be changed if needed

    def query(self, prompt: str, context: str, profile_data: str, temperature: float = 0) -> str:
        """
        Sends a query to the OpenAI GPT model using the Chat Completion endpoint.

        Args:
            prompt (str): The user's input prompt.
            profile_data (str): Additional profile data to append to the prompt.
            temperature (float): The degree of randomness in the model's output.

        Returns:
            str: The response from the GPT model.
        """

        final_prompt = f'{prompt}\ncontext: <{context}>\nprofile_data: <{profile_data}>'
        messages = [{"role": "user", "content": final_prompt}]
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
        # Logic to query the local model
        response = self.model.generate_response(input_data)
        return response


def use_language_model(api: LanguageModelAPI, input_text: str):
    return api.query(input_text)

if __name__ == "__main__":
    openai_api = OpenAIGPTAPI(OPENAI_API_KEY)
    prompt = "Translate the following English text to French:"
    from test_response import test_response
    prompt = 'Please help me construct a personalized morning briefing on my day. Use the following context and personal data to do so. My personal data includes todays data from my fitness tracker, planned tasks from my calendar, and information about todays forecast. Help contextualize things for me, understand how my health might impact my day, and tell me if my days alligns with my longterm goals.'
    context = 'I am a programmer living in Prague striving for career development while not neglecting other critical areas in life.'
    profile_data = test_response
    import logging
    from weather_api import WeatherAPI
    from fitness_api import FitnessAPI
    from motion_api import MotionAPI
    from config import *
    motion_api = MotionAPI(MOTION_API_KEY)
    clean_task_data = motion_api.get_clean_task_data()
    profile_data = clean_task_data
    response = openai_api.query(prompt, context, profile_data)
    print(response.choices[0].message.content)
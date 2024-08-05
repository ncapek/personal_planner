"""
A comprehensive module designed to integrate and automate various aspects of personal scheduling and well-being.
This module consolidates data from different sources to present a daily briefing, including weather updates,
fitness analytics, and personalized schedules. The module makes use of several specialized APIs to fetch relevant data,
and utilizes language models to generate user-friendly prompts.
"""

from bs4 import BeautifulSoup
import logging
from config import FITNESS_TEMPLATE, WEATHER_TEMPLATE, SCHEDULE_TEMPLATE, CONTEXT, CONFIG
from apis.language_model_api import OpenAIGPTAPI
from apis.data_api import CombinedDataAPI
from apis.fitness_api import FitnessAPI
from apis.weather_api import WeatherAPI
from apis.motion_api import MotionAPI
from apis.calendar_api import CalendarAPI
from apis.schedule_api import ScheduleAPI
from apis.sendgrid_api import send_email
from langchain import PromptTemplate
from dotenv import load_dotenv
from credentials_manager import CredentialsManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PromptManager:
    def __init__(self, weather_template: PromptTemplate, fitness_template: PromptTemplate,
                 schedule_template: PromptTemplate):
        """
        Initializes the PromptGenerator with specific templates for weather and fitness.
        """
        self.weather_template = weather_template
        self.fitness_template = fitness_template
        self.schedule_template = schedule_template

    def create_weather_prompt(self, weather_data: dict) -> str:
        """
        Generates a prompt for the language model using the provided weather data.
        """
        return self.weather_template.format(weather_data=weather_data)

    def create_fitness_prompt(self, fitness_data: dict) -> str:
        """
        Generates a prompt for the language model using the provided fitness data.
        """
        return self.fitness_template.format(fitness_data=fitness_data)

    def create_calendar_prompt(self, context: str, fitness_overview: dict, weather_recommendations: dict,
                               todays_schedule: dict) -> str:
        """
        Generates a prompt for the language model using the provided Motion data.
        """
        # Format the data into the template
        formatted_prompt = self.schedule_template.format(
            context=context,
            fitness_overview=fitness_overview,
            weather_recommendations=weather_recommendations,
            todays_schedule=todays_schedule
        )

        return formatted_prompt


class SectionParser:
    @staticmethod
    def parse_sections(response, section_ids):
        """
        Parses specified sections from the provided HTML response.
        """
        try:
            soup = BeautifulSoup(response, 'html.parser')
            sections = {section_id: soup.find(id=section_id) for section_id in section_ids}
            return sections
        except Exception as e:
            logger.error(f"Error occurred while parsing sections: {e}")
            return {section_id: None for section_id in section_ids}


class HTMLConstructor:
    @staticmethod
    def construct_html(sections_dict):
        """
        Constructs an HTML document with provided sections.
        """
        # Create a new BeautifulSoup object with initial HTML structure
        new_html = BeautifulSoup('<html><head><style>li { font-weight: normal; }</style></head><body></body></html>',
                                 'html.parser')

        # Add personalized greeting at the start
        greeting_header = new_html.new_tag('h1')
        greeting_header.string = f"Morning Briefing for Nicholas"
        new_html.body.append(greeting_header)

        greeting_text = new_html.new_tag('p')
        greeting_text.string = f"Good morning, Nicholas! Here's an overview of your day:"
        new_html.body.append(greeting_text)
        new_html.body.append(new_html.new_tag('br'))

        # Iterate over each main section
        for section_title, subsections in sections_dict.items():
            # Create and append the main section header
            header = new_html.new_tag('h2')
            header.string = section_title
            new_html.body.append(header)
            new_html.body.append(new_html.new_tag('br'))

            # Iterate over each subsection within the main section
            for subsection_title, content in subsections.items():
                # Append the content of the subsection if it exists
                if content:
                    new_html.body.append(content)

        # Add personalized conclusion at end
        ending_header = new_html.new_tag('br')
        new_html.body.append(ending_header)
        ending_text = new_html.new_tag('p')
        ending_text.string = f"Wishing you a productive and balanced day, Nicholas!"
        new_html.body.append(ending_text)
        ending_text = new_html.new_tag('br')
        new_html.body.append(ending_text)
        ending_text = new_html.new_tag('p')
        ending_text.string = f"Best regards,"
        new_html.body.append(ending_text)
        ending_text = new_html.new_tag('br')
        new_html.body.append(ending_text)
        ending_text = new_html.new_tag('p')
        ending_text.string = f"Your AI Assistant"
        new_html.body.append(ending_text)

        # Prettify and convert the new HTML document to a string
        return new_html.prettify()


class PersonalPlanner:
    def __init__(self, data_api: CombinedDataAPI, llm_api: OpenAIGPTAPI, prompt_manager: PromptManager, config: dict):
        self.data_api = data_api
        self.llm_api = llm_api
        self.prompt_manager = prompt_manager
        self.config = config

    def generate_daily_briefing(self, context):
        # Fetch combined data
        combined_data = self.data_api.get_combined_data(
            self.config["LATITUDE"], self.config["LONGITUDE"], self.config["TIMEZONE"], self.config["N_DAYS_AHEAD"])

        # Generate prompts for the LLM
        weather_prompt = self.prompt_manager.create_weather_prompt(combined_data['weather'])
        fitness_prompt = self.prompt_manager.create_fitness_prompt(combined_data['fitness'])

        # Get responses from the LLM
        weather_response = self.llm_api.query(weather_prompt)
        fitness_response = self.llm_api.query(fitness_prompt)

        # Parse responses into sections
        weather_sections = SectionParser.parse_sections(weather_response.choices[0].message.content,
                                                        ['weather_overview', 'weather_recommendations'])
        fitness_sections = SectionParser.parse_sections(fitness_response.choices[0].message.content,
                                                        ['fitness_overview'])
        # Handle motion part
        schedule_prompt = self.prompt_manager.create_calendar_prompt(context, fitness_sections['fitness_overview'],
                                                                     weather_sections['weather_recommendations'],
                                                                     combined_data['schedule'])
        schedule_response = self.llm_api.query(schedule_prompt)
        schedule_sections = SectionParser.parse_sections(schedule_response.choices[0].message.content,
                                                         ['daily_schedule', 'suggestions'])

        # Construct the final HTML
        html_content = HTMLConstructor.construct_html({
            'Weather Section': weather_sections,
            'Fitness Section': fitness_sections,
            'Schedule Section': schedule_sections
        })

        return html_content


def create_api_instances(credentials_manager: CredentialsManager, config: dict):
    """
    Create API instances with credentials managed. Optionally use a configuration manager
    for non-credential configurations.
    """

    weather_api = WeatherAPI(credentials_manager.get_credential('OPENWEATHER_API_KEY'))
    fitness_api = FitnessAPI(
        email=credentials_manager.get_credential('GARMIN_EMAIL'),
        password=credentials_manager.get_credential('GARMIN_PASSWORD')
    )
    motion_api = MotionAPI(credentials_manager.get_credential('MOTION_API_KEY'))
    calendar_api = CalendarAPI(
        api_url=config['CALENDER_LINK'],
        calendar_id=config['CALENDER_ID'],
        timezone=config['CALENDAR_TIMEZONE']
    )

    # Initialize ScheduleAPI with MotionAPI and CalendarAPI
    schedule_api = ScheduleAPI(motion_api=motion_api, calendar_api=calendar_api)

    # Return a dictionary of all API instances
    apis = {
        'weather_api': weather_api,
        'fitness_api': fitness_api,
        'schedule_api': schedule_api,  # Include the newly created ScheduleAPI
    }
    return apis


if __name__ == '__main__':
    load_dotenv()
    credentials_manager = CredentialsManager()

    # Create API instances
    apis = create_api_instances(credentials_manager, CONFIG)
    data_api = CombinedDataAPI(**apis)
    llm_api = OpenAIGPTAPI(credentials_manager.get_credential("OPENAI_API_KEY"))

    # prepare prompt managing object
    prompt_manager = PromptManager(
        weather_template=WEATHER_TEMPLATE,
        fitness_template=FITNESS_TEMPLATE,
        schedule_template=SCHEDULE_TEMPLATE
    )

    # prepare and send email
    planner = PersonalPlanner(data_api, llm_api, prompt_manager, CONFIG)
    daily_briefing_html = planner.generate_daily_briefing(CONTEXT)
    send_email(credentials_manager.get_credential("SENDGRID_API_KEY"), CONFIG["FROM_EMAIL"], CONFIG["TO_EMAIL"],
               CONFIG["SUBJECT"], daily_briefing_html)

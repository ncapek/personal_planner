# Personal Planner
## Overview
The Personal Planner project integrates various personal data sources such as planners, fitness trackers, financial apps, and more, into a Large Language Model (LLM) to generate personalized reports. This approach aims to provide a unified view of your daily activities, health metrics, and other personal data for more informed and tailored decision-making.

## Features
- Weather Data Integration: Fetches current weather and forecasts for your location. (openweather api)
- Fitness Data Analysis: Summarizes your daily fitness activities. (google fit data accessed via nocode.com)
- Task Management: Keeps track of your planner tasks and deadlines. (usemotion.com api)
- Personalized Reports: Generates tailored daily briefings using an LLM. (openai api)

Sample Output
```md
Good morning! Here's your personalized morning briefing:

Today in Prague, the weather is currently 0.3°C with snowfall. The forecast indicates that there will be rain and snow throughout the day, with a maximum temperature of 4.33°C and a minimum temperature of 0.3°C. However, please be aware that there is a flood alert in effect until tomorrow evening, so it's important to stay informed about any potential impacts.

Considering your fitness data, you took 1533 steps and had 20 active minutes yesterday, contributing to an expenditure of 251 calories. Your heart rate was elevated for 9 minutes, which indicates a moderate level of physical activity. Keep up the good work!

In terms of your planned tasks, you have completed a work task named "test" that was due yesterday. Great job on meeting the deadline! However, there is another work task with the same name that is due today with a duration of 30 minutes. Make sure to allocate time for its completion.

Considering your long-term goals as a programmer striving for career development, it's important to balance your work tasks with other critical areas of life. Take a moment to assess your overall schedule for the day and ensure that you have allocated time for personal growth, relaxation, and any other activities that align with your long-term goals.

Given the weather conditions and the flood alert, it might be a good idea to plan for indoor activities or avoid risky areas. Consider utilizing this time to focus on tasks that can be done remotely or from the comfort of your home.

Remember to stay aware of any updates regarding the weather and flood alert throughout the day. Stay motivated, take breaks, and make sure your schedule aligns with your long-term goals. Have a productive and successful day!
```

# Getting Started
## Prerequisites
Access to APIs (OpenWeather, Google Fit accessed via NoCode, Motion Planner, OpenAI GPT).

## Installation

Clone the repository:

```bash
git clone https://github.com/ncapek/personal_planner.git
```
Install required dependencies:

```bash
pip install -r requirements.txt
```

Configuration
Set up your API keys and endpoints in config.py.

To run the planner:

```bash
python main.py
```

# How It Works
Data Retrieval: The application fetches data from the specified APIs.

Data Processing: Cleans and formats the data for input into the LLM.

Querying the LLM: Sends the compiled data to an LLM (like OpenAI's GPT) for generating the report.

Output: Displays a personalized daily briefing based on the processed data.

## Customization

Modify config.py to personalize API endpoints and keys.
Adjust the data extraction and processing methods for tailored outputs.
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

class UdemyAPI:
    def __init__(self):
        """Initializes the UdemyAPI with the option to run Chrome in headless mode."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ensures Chrome runs in headless mode
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        #chrome_options.add_argument("--disable-gpu")  # Disables GPU hardware acceleration
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
        #chrome_options.add_argument("--disable-dev-shm-usage")  # Overcomes limited resource problems     
        #chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        #chrome_options.add_experimental_option('useAutomationExtension', False)

        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)


    def get_courses(self, topic, max_results=10, language='en', min_rating=3.5, sort='newest'):
        """
        Fetches courses on a given topic from Udemy with specified filters.

        Args:
            topic (str): The topic for which to fetch courses (e.g., 'machine learning').
            max_results (int): Maximum number of courses to fetch.
            language (str): Language filter for the courses.
            min_rating (float): Minimum rating filter for the courses.
            sort (str): Sorting criteria for the courses (e.g., 'newest', 'highest-rated').

        Returns:
            list: A list of tuples containing course titles and URLs.
        """
        url = f"https://www.udemy.com/courses/search/?src=ukw&q={topic}&lang={language}&ratings={min_rating}&sort={sort}"
        self.driver.get(url)

        # Wait for the dynamic content to load
        time.sleep(5)  # Adjust the sleep time if necessary

        # Find course elements and extract data
        courses = []
        for course in self.driver.find_elements(By.CLASS_NAME, 'course-card-module--main-content--3Uvsz')[:max_results]:
            title = course.find_element(By.CLASS_NAME, 'course-card-title-module--title--2C6ac').text.strip()
            course_url = course.find_element(By.TAG_NAME, 'a').get_attribute('href')
            courses.append((title, course_url))

        return courses

    def close(self):
        """Closes the Selenium webdriver."""
        self.driver.quit()

# Example usage
if __name__ == "__main__":
    udemy_api = UdemyAPI()
    try:
        newest_courses = udemy_api.get_courses("machine+learning", 10, language='en', min_rating=3.5, sort='newest')
        for title, url in newest_courses:
            print(f"Course: {title}, URL: {url}")
    finally:
        udemy_api.close()

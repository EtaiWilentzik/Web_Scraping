from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from BaseJob import BaseJob


class Drushim(BaseJob):
    def __init__(self):
        super().__init__()
        self.job_list = []
        self.url = "https://www.drushim.co.il/jobs/cat6/?experience=1-2&ssaen=3"
        self.html = None

    def next_page(self, page_number):
        # Override next_page to just return the first page's content or nothing
        if page_number == 1:
            self.get_bottom()
            soup = BeautifulSoup(self.html, "html.parser")
            return soup
        return None  # Return None for other page numbers to avoid unnecessary calls

    def get_bottom(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode

        driver = webdriver.Chrome(options=chrome_options)  # Pass options to the WebDriver
        driver.set_page_load_timeout(15)  # Set page load timeout
        driver.get(self.url)

        start_time = time.time()  # Record start time

        try:
            while True:
                try:
                    button = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'load_jobs_btn')]"))
                    )
                    driver.execute_script("arguments[0].click();", button)
                    WebDriverWait(driver, 3).until(EC.staleness_of(button))
                except:
                    print("No more 'Load More' button found. Finishing crawl.")
                    break
        finally:
            self.html = driver.page_source
            driver.quit()

        end_time = time.time()  # Record end time
        total_time = end_time - start_time  # Calculate total time taken
        print(f"Total time taken for crawling: {total_time:.2f} seconds")

    def read_page(self, soup, job_list, optional_names):
        jobs = soup.find_all("div", class_="pt-0 mb-6 jobList_vacancy")
        for job in jobs:
            job_title_div = job.find("span", class_="job-url primary--text font-weight-medium primary--text")
            if job_title_div:
                job_title = job_title_div.text.lower().replace('\n', ' ').replace('\t', ' ').replace('  ',
                                                                           ' ').strip()
                if any(word in job_title for word in optional_names):
                    job_date_div = job.find("span", class_="display-18 inline-flex")
                    job_date = job_date_div.text if job_date_div else "Unknown Date"
                    job_description_element = job.find_all("div", class_="flex xs12")
                    job_description = ""
                    for item in job_description_element:
                        job_description += item.text.strip() + "\n "
                    job_description = job_description.strip() if job_description else "No description available"
                    company_div = job.find("a", class_="black--text disabledLink no-underline")
                    company_link = company_div['href'].strip() if company_div else "No company link available"
                    company_name = company_div.text.strip() if company_div else "Unknown Company"

                    new_job = {
                        "title": job_title,
                        "posted_date": job_date,
                        "requirements": job_description,
                        "company_name": company_name,
                        "company_link": company_link
                    }

                    job_list.append(new_job)



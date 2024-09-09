import certifi
import requests
from bs4 import BeautifulSoup

from BaseJob import BaseJob


class JobMaster(BaseJob):
    def __init__(self):
        self.job_list = []
        super().__init__(
            "https://www.jobmaster.co.il/jobs/?currPage={page_number}&q=%D7%9E%D7%97%D7%A9%D7%91%D7%99%D7%9D+%D7%95%D7%AA%D7%95%D7%9B%D7%A0%D7%94")

    def read_page(self, soup, job_list, optional_names):

        jobs = soup.find_all('article', class_="CardStyle JobItem font14")
        for job in jobs:

            job_title = "Unknown Title"
            company_div = job.find("a", class_="CardHeader View_Job_Details")
            if company_div:
                company_link = "https://www.jobmaster.co.il" + company_div['href']

                job_title = company_div.text.lower().replace('\n', ' ').replace('\t', ' ').replace('  ',
                                                                                                   ' ').strip()
                if any(word in job_title for word in optional_names):
                    posted_date_element = job.find("span", class_="Gray")
                    posted_date = posted_date_element.text.strip() if posted_date_element else "Unknown Date"
                    # print(posted_date)
                    # print("the company link is ", company_link)
                    company_name_element = job.find("a", class_="CompanyNameLink")
                    company_name = company_name_element.text.strip() if company_name_element else "Unknown Company"

                    company_description = self.open_job_link(company_link)

                    new_job = {
                        "title": job_title,
                        "posted_date": posted_date,
                        "requirements": company_description,
                        "company_name": company_name,
                        "company_link": company_link
                    }
                    job_list.append(new_job)

    def open_job_link(self, url):
        soup = self.get_soup(url)
        job_description = soup.find("div", class_="jobDescription")
        job_requirements = soup.find("div", class_="jobRequirements")
        res = job_description.text.strip() + "\n" + job_requirements.text.strip() if (
                    job_description and job_requirements) else "No description available"
        # print(res)
        return res

    def get_soup(self, url):

        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        }
        # print("URL: ", url)
        response = requests.get(url, headers=header, verify=certifi.where())
        soup = BeautifulSoup(response.text, "html.parser")
        # print("+====================++====================++====================+")
        # print("Page number: ", page_number)
        return soup

import requests
from bs4 import BeautifulSoup

from BaseJob import BaseJob


class GotFriends(BaseJob):

    def __init__(self):
        self.job_list = []
        super().__init__("https://www.gotfriends.co.il/jobslobby/software/?page={page_number}&total=979")

    def next_page(self, page_number):
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        }
        url = self.url.format(page_number=page_number)
        # print("URL: ", url)
        response = requests.get(url, headers=header, verify=False)  #this the reason im using this method verify=False.
        soup = BeautifulSoup(response.text, "html.parser")
        # print("+====================++====================++====================+")
        # print("Page number: ", page_number)
        return soup

    def read_page(self, soup, job_list, optional_names):

        ## find all the jobs in the page
        jobs = soup.find_all('div', class_="item")
        for job in jobs:
            job_title = "Unknown Title"
            company_div = job.find("a")
            if company_div:

                company_link = "https://www.gotfriends.co.il" + company_div['href']
                job_title = company_div.text.lower().replace('\n', ' ').replace('\t', ' ').replace('  ',
                                                                                                   ' ').strip()
                if any(word in job_title for word in optional_names):
                    # print("__________________________")
                    # print(job_title)
                    job_description_element = job.find_all("div", class_="desc")
                    job_description = ""
                    for item in job_description_element:
                        job_description += item.text.strip() + "\n "
                    job_description = job_description.strip() if job_description else "No description available"

                    new_job = {
                        "title": job_title,
                        "posted_date": "Unknown Date",
                        "requirements": job_description,
                        "company_name": "Unknown Company",
                        "company_link": company_link
                    }
                    job_list.append(new_job)
from BaseJob import BaseJob


class AllJob(BaseJob):
    def __init__(self):
        self.job_list = []
        super().__init__(
            "https://www.alljobs.co.il/SearchResultsGuest.aspx?page={page_number}&position=1994,1733,259,1799,1905,1074,1880,1111,244,245,749,1203,1154,1759,1230,1712,1153,1711,1731,1883&type=&source=&duration=0&exc=&region=")

    def read_page(self, soup, job_list, optional_names):

        ## find all the jobs in the page
        jobs = soup.find_all('div', class_="open-board")
        for job in jobs:
            job_content = job.find("div", class_="job-content-top")
            if job_content:
                job_title_element = job_content.find("h2")
                job_title = job_title_element.text.lower().replace('\n', ' ').replace('\t', ' ').replace('  ',
                                                                                                         ' ').strip() if job_title_element else "Unknown Title"
                # print(job_title)
                #check if the job title contains any substring of the optional names
                if any(word in job_title for word in optional_names):
                    # print(job_title)
                    job_date_element = job_content.find("div", class_="job-content-top-date")
                    job_date = job_date_element.text if job_date_element else "Unknown Date"

                    job_description_element = job_content.find("div", class_="job-content-top-desc AR RTL")
                    job_description = job_description_element.text.strip() if job_description_element else "No description available"

                    company_div = job_content.find("a", class_="L_Blue gad addFocus")

                    company_link = None
                    if company_div:
                        company_link = "https://www.alljobs.co.il"+company_div['href']
                        # print(company_link)
                    else:
                        company_link = "No company link available"

                    company_name_element = job_content.find("div", class_="T14")
                    company_name = company_name_element.a.text if company_name_element and company_name_element.a else "Unknown Company"

                    # print(company_name)
                    # print(job_description.text.strip())
                    # print(job_date)  # Print the text of the found element
                    new_job = {
                        "title": job_title,
                        "posted_date": job_date,
                        "requirements": job_description,
                        "company_name": company_name,
                        "company_link": company_link
                    }

                    job_list.append(new_job)
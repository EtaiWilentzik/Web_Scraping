import threading
import time

import warnings
from urllib3.exceptions import InsecureRequestWarning
from files import create_csv_from_list, create_excel_from_list2
from AllJob import AllJob
from Drushim import Drushim
from GotFriends import GotFriends
from Jobmaster import JobMaster

# Suppress only InsecureRequestWarning warnings
warnings.simplefilter('ignore', InsecureRequestWarning)


# class AllJob(BaseJob):
#     def __init__(self):
#         self.job_list = []
#         super().__init__(
#             "https://www.alljobs.co.il/SearchResultsGuest.aspx?page={page_number}&position=1994,1733,259,1799,1905,1074,1880,1111,244,245,749,1203,1154,1759,1230,1712,1153,1711,1731,1883&type=&source=&duration=0&exc=&region=")
#
#     def read_page(self, soup, job_list, optional_names):
#
#         ## find all the jobs in the page
#         jobs = soup.find_all('div', class_="open-board")
#         for job in jobs:
#             job_content = job.find("div", class_="job-content-top")
#             if job_content:
#                 job_title_element = job_content.find("h2")
#                 job_title = job_title_element.text.lower().replace('\n', ' ').replace('\t', ' ').replace('  ',
#                                                                                                          ' ').strip() if job_title_element else "Unknown Title"
#                 # print(job_title)
#                 #check if the job title contains any substring of the optional names
#                 if any(word in job_title for word in optional_names):
#                     # print(job_title)
#                     job_date_element = job_content.find("div", class_="job-content-top-date")
#                     job_date = job_date_element.text if job_date_element else "Unknown Date"
#
#                     job_description_element = job_content.find("div", class_="job-content-top-desc AR RTL")
#                     job_description = job_description_element.text.strip() if job_description_element else "No description available"
#
#                     company_div = job_content.find("a", class_="L_Blue gad addFocus")
#
#                     company_link = None
#                     if company_div:
#                         company_link = "https://www.alljobs.co.il" + company_div['href']
#                         # print(company_link)
#                     else:
#                         company_link = "No company link available"
#
#                     company_name_element = job_content.find("div", class_="T14")
#                     company_name = company_name_element.a.text if company_name_element and company_name_element.a else "Unknown Company"
#
#                     # print(company_name)
#                     # print(job_description.text.strip())
#                     # print(job_date)  # Print the text of the found element
#                     new_job = {
#                         "title": job_title,
#                         "posted_date": job_date,
#                         "requirements": job_description,
#                         "company_name": company_name,
#                         "company_link": company_link
#                     }
#
#                     job_list.append(new_job)


# class GotFriends(BaseJob):
#
#     def __init__(self):
#         self.job_list = []
#         super().__init__("https://www.gotfriends.co.il/jobslobby/software/?page={page_number}&total=979")
#
#     def next_page(self, page_number):
#         header = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
#         }
#         url = self.url.format(page_number=page_number)
#         # print("URL: ", url)
#         response = requests.get(url, headers=header, verify=False)  #this the reason im using this method verify=False.
#         soup = BeautifulSoup(response.text, "html.parser")
#         # print("+====================++====================++====================+")
#         # print("Page number: ", page_number)
#         return soup
#
#     def read_page(self, soup, job_list, optional_names):
#
#         ## find all the jobs in the page
#         jobs = soup.find_all('div', class_="item")
#         for job in jobs:
#             job_title = "Unknown Title"
#             company_div = job.find("a")
#             if company_div:
#
#                 company_link = "https://www.gotfriends.co.il" + company_div['href']
#                 job_title = company_div.text.lower().replace('\n', ' ').replace('\t', ' ').replace('  ',
#                                                                                                    ' ').strip()
#                 if any(word in job_title for word in optional_names):
#                     # print("__________________________")
#                     # print(job_title)
#                     job_description_element = job.find_all("div", class_="desc")
#                     job_description = ""
#                     for item in job_description_element:
#                         job_description += item.text.strip() + "\n "
#                     job_description = job_description.strip() if job_description else "No description available"
#
#                     new_job = {
#                         "title": job_title,
#                         "posted_date": "Unknown Date",
#                         "requirements": job_description,
#                         "company_name": "Unknown Company",
#                         "company_link": company_link
#                     }
#                     job_list.append(new_job)


def get_optional_names():
    optional_names = [
        # Existing English terms (development-focused)
        "software junior", "sw junior", "junior software", "junior sw", "junior developer", "junior  software ",
        "junior software developer", "junior  software  engineer",
        "junior programmer", "junior engineer", "junior software engineer",
        "junior software developer", "junior software programmer",
        "junior full stack", "junior full stack developer",
        "entry level developer", "entry level software engineer", "entry level programmer",
        "entry level engineer", "entry level full stack developer",
        "junior backend developer", "junior frontend developer", "junior mobile developer",
        "junior data engineer", "junior data scientist", "junior machine learning engineer",
        "junior ai developer", "junior web developer", "junior android developer",
        "junior ios developer", "junior cloud engineer", "junior network engineer",
        "graduate developer", "graduate software engineer", "graduate programmer",
        "graduate software developer", "graduate software programmer",
        "associate software developer", "associate engineer", "associate software engineer",
        "associate programmer", "junior python developer", "junior java developer",
        "junior c# developer", "junior javascript developer", "junior react developer",
        "junior node.js developer", "junior golang developer", "junior kotlin developer",
        "junior c++ developer", "junior c developer", "Junior Automation"

        # New English terms (development-focused)
                                                      "junior vue developer", "junior angular developer",
        "junior typescript developer",
        "junior ruby developer", "junior ruby on rails developer", "junior php developer",
        "junior laravel developer", "junior scala developer", "junior rust developer",
        "junior swift developer", "junior flutter developer", "junior react native developer",
        "junior unity developer", "junior unreal engine developer", "junior blockchain developer",
        "junior smart contract developer", "junior shopify developer", "junior wordpress developer",
        "junior magento developer", "junior salesforce developer", "junior tableau developer", "junior sap developer",
        "junior oracle developer",
        "junior sql developer", "junior nosql developer", "junior mongodb developer",
        "junior postgresql developer", "junior mysql developer", "junior graphql developer",
        "junior api developer", "junior microservices developer", "junior serverless developer",
        "junior embedded systems programmer", "junior firmware developer", "junior iot developer",
        "junior ar/vr developer", "junior computer vision developer", "junior nlp developer",

        # Existing Hebrew terms (development-focused)
        "מפתח מתחיל", "מפתח תוכנה מתחיל", "מהנדס תוכנה מתחיל", "מפתח תוכנה זוטר",
        "תוכניתן מתחיל", "מפתח/ת full stack junior", "מפתח /ת FullStack junior!",
        "מפתח/ת REACT מתחיל/ה", "מפתח.ת תוכנה מתחיל.ה", "מפתח אפליקציות מתחיל",

        # New Hebrew terms (development-focused)
        "מתכנת/ת מתחיל/ה", "מפתח/ת ג'וניור", "מהנדס/ת תוכנה זוטר/ה",
        "מפתח/ת בק-אנד מתחיל/ה", "מפתח/ת פרונט-אנד מתחיל/ה",
        "מפתח/ת מובייל מתחיל/ה", "מהנדס/ת נתונים מתחיל/ה",
        "מדען/ית נתונים מתחיל/ה", "מהנדס/ת למידת מכונה מתחיל/ה",
        "מפתח/ת בינה מלאכותית מתחיל/ה", "מפתח/ת אתרים מתחיל/ה",
        "מפתח/ת אנדרואיד מתחיל/ה", "מפתח/ת iOS מתחיל/ה",
        "מפתח/ת משחקים מתחיל/ה", "מפתח/ת פייתון מתחיל/ה",
        "מפתח/ת ג'אווה מתחיל/ה", "מפתח/ת C# מתחיל/ה",
        "מפתח/ת ג'אווהסקריפט מתחיל/ה", "מפתח/ת Node.js מתחיל/ה",
        "מפתח/ת Go מתחיל/ה", "מפתח/ת Kotlin מתחיל/ה",
        "מפתח/ת C++ מתחיל/ה", "מפתח/ת C מתחיל/ה",
        "מפתח/ת TypeScript מתחיל/ה",
        "מפתח/ת Laravel מתחיל/ה", "מפתח/ת Scala מתחיל/ה",
        "מפתח/ת Rust מתחיל/ה", "מפתח/ת Swift מתחיל/ה",
        "מפתח/ת Flutter מתחיל/ה", "מפתח/ת React Native מתחיל/ה",
        "מפתח/ת SQL מתחיל/ה", "מפתח/ת NoSQL מתחיל/ה",
        "מפתח/ת MongoDB מתחיל/ה", "מפתח/ת AR/VR מתחיל/ה", "מפתח/ת ראייה ממוחשבת מתחיל/ה",
        "מפתח/ת NLP מתחיל/ה", "מנהל /ת פרויקטי  ERP", "מפתח /ת Full Stack Junior", " מפתח /ת ללא ניסיון",
        "תוכניתן ללא ניסיון", "תואר במדעי המחשב", "תואר מדעי המחשב", "Data Engineer Junior", "Data Scientist Junior",
        "Machine Learning Junior",
        "AI Junior", "Web Junior", "Android Junior", "IOS Junior", "Cloud Junior", "Network Junior",
        "Graduate Developer", "Graduate Software Engineer", "Graduate Programmer"
        # , "Data Engineer", "BI Developer",


    ]
    for i in range(len(optional_names)):
        optional_names[i] = optional_names[i].lower().replace('\n', ' ').replace('\t', ' ').replace('  ', ' ').strip()
    return optional_names


#
def scrape_site_sequential(site, num_of_pages):
    job_list = []
    optional_names = get_optional_names()
    for i in range(1, num_of_pages + 1):
        soup = site.next_page(i)
        if soup:  # Ensure there's content before calling read_page
            site.read_page(soup, job_list, optional_names)
        if isinstance(site, Drushim):  # If it's Drushim, stop after the first page
            break
    return job_list



def scrape_all_sites_sequential(sites, num_of_pages):
    job_list = []
    for site in sites:
        job_list += scrape_site_sequential(site, num_of_pages)
    return job_list


def scrape_site_threaded(site, num_of_pages, job_list, lock, optional_names):
    local_job_list = []

    for i in range(1,num_of_pages+1,1):#start from 1 because the first page is 1 and not 0
        soup = site.next_page(i)

        if soup:
            site.read_page(soup, local_job_list, optional_names)
        if isinstance(site, Drushim):  # Stop after first page for Drushim
            break

    # Add local results to shared job_list
    with lock:
        job_list.extend(local_job_list)


def scrape_all_sites_threaded(sites, num_of_pages):
    job_list = []
    lock = threading.Lock()
    optional_names = get_optional_names()
    threads = []

    for site in sites:
        thread = threading.Thread(target=scrape_site_threaded,
                                  args=(site, num_of_pages, job_list, lock, optional_names))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    return job_list


if __name__ == "__main__":

    start_time = time.time()
    # sites = [AllJob(),GotFriends(),JobMaster(),Drushim()]
    sites = [AllJob(),GotFriends()]
    #
    # jobs = scrape_all_sites_threaded(sites, 30)
    jobs = scrape_all_sites_sequential(sites, 30)
    print("Results:")
    for job in jobs:
        print("__________________________")
        print("the title is ", job["title"])
        print("date ", job["posted_date"])
        print("the requirements is ", job["requirements"])
        print("the company name is ", job["company_name"])
        print("the company link is ", job["company_link"])


    end_time = time.time()
    print("Execution time: ", end_time - start_time)  # Print the execution time
    print(f"Total jobs found: {len(jobs)}")
    create_csv_from_list(jobs, "jobs.csv")
    create_excel_from_list2(jobs, "jobs1.csv")


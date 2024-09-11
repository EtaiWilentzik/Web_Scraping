# Job Scraper

## General Information
This repository contains a job scraping tool that collects job listings from various websites and compiles them into a single dataset. The tool supports both sequential and threaded scraping to optimize performance.

The tool scrapes job listings from multiple websites, exports the collected data to an Excel file, and can send an email with the collected job listings as an attachment.

The project was written using Python.

## Setup
1. Make sure you have Python 3.x installed on your local machine.
2. Clone the repository:
```
git clone https://github.com/EtaiWilentzik/job-scraper.git
cd job-scraper
```
3. Install the required packages:
```
pip install -r requirements.txt
```

### Usage
1. **Run the Scraper**:
    ```sh
    python main.py
    ```

2. **Configuration**:
    - Modify the `sites` list in the `main.py` file to include the websites you want to scrape.
    - Adjust the number of pages to scrape by changing the `num_of_pages` parameter.

3. **Output**:
    - The results will be printed to the console.
    - An Excel file named `data.xlsx` will be created with the collected job listings.

### Functions
- `get_optional_names()`: Returns a list of optional job titles to search for.
- `scrape_site_sequential(site, num_of_pages)`: Scrapes a single site sequentially.
- `scrape_all_sites_sequential(sites, num_of_pages)`: Scrapes all sites sequentially.
- `scrape_site_threaded(site, num_of_pages, job_list, lock, optional_names)`: Scrapes a single site using threading.
- `scrape_all_sites_threaded(sites, num_of_pages)`: Scrapes all sites using threading.

### Example
```python
if __name__ == "__main__":
    start_time = time.time()
    sites = [AllJob(), GotFriends(), JobMaster(), Drushim()]
    jobs = scrape_all_sites_threaded(sites, 700)
    print("Results:")
    for job in jobs:
        print("__________________________")
        print("the title is ", job["title"])
        print("date ", job["posted_date"])
        print("the requirements is ", job["requirements"])
        print("the company name is ", job["company_name"])
        print("the company link is ", job["company_link"])
    end_time = time.time()
    print("Execution time: ", end_time - start_time)
    print(f"Total jobs found: {len(jobs)}")
    create_excel_from_list2(jobs)
```

## Built with
- Python

## Author
**Etai Wilentzik**
* [Profile](https://github.com/EtaiWilentzik)

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Support 🤝
Contributions, issues, and feature requests are welcome!

Give a ⭐️ if you like this project!

# 🗺️ Google Maps Scraper

A Python-based web scraper designed to collect **business information from Google Maps**, including company name, address, phone number, and website.  
The script also visits each business's website to extract available **email addresses** for lead generation and data enrichment purposes.

---
This scrapper project consists of three main Python scripts, each handling a different part of the workflow:
1. Googlemaps.py 
This script contains the core scraping logic. 
It connects to Google Maps using Playwright, performs searches based on the provided keywords, and extracts business details such as company name, address, phone number, website, and email (if available)
2. runner.py 
This script servers as the controller or automation runner for the scraper. 
Here you define:
- The list of cities you want to scrape 
- The keywords (e.g. "pool builder", "pool remodeler", etc)
- The number of results to collect for each city when executed, it automatically runs the scraper for each combination you specify
3. cleaner.py 
This script handles the data cleaning and normalization process after scraping. 
It standardizes fields such as phone numbers, website domains, and addresses to make the dataset consistent and ready for use (e.g., uploading to a CRM or dashboard)

Note: The current version of cleaner.py is specifically designed to clean U.S. -based business data. Since address and contact formats differ across countries, this script may not properly clean data scraped from other regions without some modificaton

## How to Use This Script

1. **Clone the repository** to your local computer:
   ```bash
   git clone https://github.com/belamon/Google-Maps-Sraper.git
   cd Google-Maps-Sraper

2. Run the script in your terminal:
    On a Mac, the command to run a Python script is typically:
    ```bash
    python3 runner.py
    ```

3. The scraper will collect business data from Google Maps, visit each business website, and extract any available email addresses it finds.
4. 	All results will be saved automatically to a CSV file inside your project folder.
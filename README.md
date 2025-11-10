# 🗺️ Google Maps Scraper

A Python-based web scraper designed to collect **business information from Google Maps**, including company name, address, phone number, and website.  
The script also visits each business's website to extract available **email addresses** for lead generation and data enrichment purposes.

---

## How to Use This Script

1. **Clone the repository** to your local computer:
   ```bash
   git clone https://github.com/belamon/Google-Maps-Sraper.git
   cd Google-Maps-Sraper

2. Run the script in your terminal:
    ```bash
    python Googlemaps.py -s "your search keyword" -t 50
    ```

    Example
     ```bash
    python Googlemaps.py -s "Pool Builder in Tampa" -t 50
    ```
    Arguments:
    -s = serach keyword (e.g "pool builder in Tampa")
    -t = total number of businesses to scrape

3. The scraper will collect business data from Google Maps, visit each business website, and extract any available email addresses it finds.
4. 	All results will be saved automatically to a CSV file inside your project folder.
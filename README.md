# Google-Maps-Sraper
A Python-based web scraper designed to collect business information from Google Maps, including company name, address, phone number, and website. The script also visits each business's website to extract available email addresses for lead-generation and data enrichment purposes.
## How to Use This Script 
1. Clone the repository to your local computer
2. Run the script in your terminal 
python Googlemaps.py -s "your search keyword" -t 50

Example:
python Googlemaps.py -s "pool builder in Florida" -t 50

-s : search keyword (e.g "pool builder in Tampa")
-t : total number of businesses to scraoe 

3. The scraper will collect business data from Google Maps, visit each business website, and extract any available email adresses it finds 
4. All result will be saved automatically to a CSV file inside your project folder. 
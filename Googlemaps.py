from playwright.sync_api import sync_playwright #import Playwright so we can control Chromium
from dataclasses import dataclass, asdict, field # import tools to define lightweight data containers, convert them to dicts, and set defauult field
import pandas as pd #to save tabular dataframe
import argparse #import CLI argument parses for -s and -t flags 
import os #file system helpers (to check folder is exists, join paths and make directories)
import sys #system features 
import re #regular expression to detect email patterns in HTML
from urllib.parse import unquote #to encode url-encoded strings 


@dataclass
class Business:
    """Lead format that matches the client's requested columns
    """
    search_keyword:str = None
    recipient_contact_name:str= None
    recipient_company:str = None 
    recipient_line_1:str = None 
    recipient_line_2:str = None
    recipient_email:str = None
    city :str=None
    recipient_phone_number :str = None
    website :str = None 
    source :str = "Google Map"
    

@dataclass
class BusinessList:
    """Hold list of business objects and save to Excel/CSV
    """
    business_list : list[Business] = field(default_factory=list) #start with an empty python list to collect many business items
    save_at : str = "output" #folder where we will save the files

    def dataframe(self):
        """Convert business_list to pandas datafram
        """
        return pd.json_normalize(
        (asdict(business)for business in self.business_list), sep="_"
        )
    def save_to_excel(self, filename:str):
        """Save pandas dataframe to excel (xlsx) file

        Args:
            filename (str): _description_
        """
        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)
        self.dataframe().to_excel(f"{self.save_at}/{filename}.xlsx", index= False)

    def save_to_csv(self, filename:str):
        """Save the leads to csv

        Args:
            filename (str): _description_
        """
        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)
        self.dataframe().to_csv(f"{self.save_at}/{filename}.csv", index=False)

def extract_email_from_website(browser,url):
    if not url:
        return "" # no website? bail and return empty string
    if not url.startswith(("http://", "https://")):
        url = "https://" + url #normalize bare domains to a full URL

    try:
        page = browser.new_page()
        page.goto(url, timeout=10000, wait_until="domcontentloaded")
        # open the site and wwait until basic DOm is ready(10s timeout)

        # look for mailto links
        links = page.locator("//a[contains(@href,'mailto:')]").all()
        # select all anchor tags with href containing 'mailto:
        for a in links:
            href = a.get_attribute("href") or ""
            href = unquote(href).replace("mailto:", "").split("?")[0].strip()
            if "@" in href:
                page.close()
                return href #if this looks like an email, return it (close page first)

        # fallback: search in page text
        html = page.content()
        match = re.search(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", html) #apply a broad email regex to the HTML
        page.close()
        if match:
            return match.group(0)
    except Exception:
        pass
    return ""

def main():
    #read search for arguments 
    parser = argparse.ArgumentParser() #create argument parses
    parser.add_argument("-s","--search", type=str) # example -s "pool builders Australia"
    parser.add_argument("-t","--total", type=int) #limit for how many listings to scrape 
    args = parser.parse_args() #parse teh CLI args into 'args'

    #build search list 
    if args.search:
        search_list = [args.search] #if -s is provided, use it as a one-item list 
    
    if args.total:
        total = args.total
    else:
        total = 1_000_000

    if not args.search:
        search_list = []
        # read search from input.txt file
        input_file_name = 'input.txt'
        # Get the absolute path of the file in the current working directory
        input_file_path = os.path.join(os.getcwd(), input_file_name)
        # Check if the file exists
        if os.path.exists(input_file_path):
        # Open the file in read mode
            with open(input_file_path, 'r') as file:
            # Read all lines into a list
                search_list = file.readlines()
                
        if len(search_list) == 0:
            print('Error occured: You must either pass the -s search argument, or add searches to input.txt')
            sys.exit()#if no -s and lines in input.txt print helpful error and exit 

        
    #Scraping 
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page() #one tab to drive Maps search and scrolling 

        page.goto("https://www.google.com/maps", timeout= 6000)
        page.wait_for_timeout(5000) #navigate to Google Maps the give the page 5s to settle

        for search_for_index, search_for in enumerate(search_list):
            print(f"-----\n{search_for_index}-{search_for}".strip()) #log which search is running 

            page.locator('//input[@id="searchboxinput"]').fill(search_for)
            page.wait_for_timeout(3000) #type the search into the main search bar and wait briefly 

            page.keyboard.press("Enter")
            page.wait_for_timeout(5000) #execute the search and wait for results to render

            #scrolling 
            page.hover('//a[contains(@href, "https://www.google.com/maps/place")]')

            # this variable is used to detect if the bot
            # scraped the same number of listings in the previous iteration
            previously_counted = 0
            while True:
                page.mouse.wheel(0,1000)
                page.wait_for_timeout(3000)
                # scroll down the left results list and wait for it to render

                if (
                    page.locator(
                        '//a[contains(@href, "https://www.google.com/maps/place")]'
                    ).count()
                    >= total
                ):
                    listings = page.locator(
                        '//a[contains(@href, "https://www.google.com/maps/place")]'
                    ).all()[:total]
                    listings = [listing.locator("xpath=..") for listing in listings]
                    print(f"Total Scraped: {len(listings)}")
                    break
                else:
                    # logic to break from loop to not run infinitely
                    # in case arrived at all available listings
                    if (
                        page.locator(
                            '//a[contains(@href, "https://www.google.com/maps/place")]'
                        ).count()
                        == previously_counted
                    ):
                        listings = page.locator(
                            '//a[contains(@href, "https://www.google.com/maps/place")]'
                        ).all()
                        print(f"Arrived at all available\nTotal Scraped: {len(listings)}")
                        break
                    else:
                        previously_counted = page.locator(
                            '//a[contains(@href, "https://www.google.com/maps/place")]'
                        ).count()
                        print(
                            f"Currently Scraped: ",
                            page.locator(
                                '//a[contains(@href, "https://www.google.com/maps/place")]'
                            ).count(),
                        )

            business_list = BusinessList() #start an empty accumulator for business rows for this query 

            #scraping 

            for listing in listings:
                try:
                    listing.click()
                    page.wait_for_timeout(5000)

                    #xpath selectors
                    recipient_company_xpath= '//h1[contains(@class, "DUwDvf")]'
                    recipient_line_1_xpath= '//button[@data-item-id="address"]//div[contains(@class,"fontBodyMedium")]'
                    city_xpath= '//button[@data-item-id="oloc"]//div[contains(@class,"fontBodyMedium")]'
                    recipient_phone_number_xpath= '//button[starts-with(@data-item-id,"phone:tel")]//div[contains(@class,"fontBodyMedium")]'
                    website_xpath= '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
                    
                   
                    business = Business()
                    #new row 
                   
                    business.search_keyword = search_for.strip() #record which term produced this row
                    loc = page.locator(recipient_company_xpath)
                    if loc.count()>0:
                        business.recipient_company=loc.first.inner_text().strip()
                    else:
                        business.recipient_company=""
                    address_nodes = page.locator(recipient_line_1_xpath)
                    if address_nodes.count() >0:
                        texts = [node.inner_text().strip() for node in address_nodes.all()]
                        business.recipient_line_1 = texts[0] if len(texts) >=1 else ""
                        business.recipient_line_2 = texts[1] if len(texts) >=2 else ""
                    else:
                        business.recipient_line_1 = ""
                        business.recipient_line_2 = ""
                    if page.locator(city_xpath).count() >0:
                        business.city = page.locator(city_xpath).all()[0].inner_text()
                    else:
                        business.city = ""
                    if page.locator(website_xpath).count() > 0:
                        business.website = page.locator(website_xpath).all()[0].inner_text()
                    else:
                        business.website = ""
                    if business.website:
                        business.recipient_email = extract_email_from_website(browser, business.website)
                    else:
                        business.recipient_email=""
                    if page.locator(recipient_phone_number_xpath).count() > 0:
                        business.recipient_phone_number = page.locator(recipient_phone_number_xpath).all()[0].inner_text()
                    else:
                        business.recipient_phone_number = ""
                    
                    business_list.business_list.append(business)
                
                except Exception as e:
                    print(f'Error occured: {e}')
            
            #########
            # output
            #########
            business_list.save_to_excel(f"google_maps_data_{search_for}".replace(' ', '_'))
            business_list.save_to_csv(f"google_maps_data_{search_for}".replace(' ', '_'))

        browser.close()


if __name__ == "__main__":
    main()
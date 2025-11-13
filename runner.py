import os 
import time
from Googlemaps import scrape 

CITIES = [
    "New York",
    "Pennsylvania"
    
]

KEYWORD = "pizza store"
TOTAL = 5
WAIT_SECONDS = 20 

PYTHON_CMD = "python3"
for city in CITIES:
    search = (f"{KEYWORD} in {city}")
    cmd = f'{PYTHON_CMD} Googlemaps.py -s "{search}" -t {TOTAL}'
    print(f"\nRunning: {cmd}")
    os.system(cmd)

    print(f"Waiting {WAIT_SECONDS} seconds")
    time.sleep(WAIT_SECONDS)

print("THE SCRAPING IS COMPLETE")


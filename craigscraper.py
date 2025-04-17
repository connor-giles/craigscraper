import re
import requests
from bs4 import BeautifulSoup
import time
import random
time.sleep(random.uniform(2, 5))  # Random delay between 2 and 5 seconds

import json

# Basic config
urls = [
    'https://orlando.craigslist.org/search/cta?query=honda+civic&purveyor=owner&max_price=10000&max_auto_miles=110000',
    'https://daytona.craigslist.org/search/cta?query=honda+civic&purveyor=owner&max_price=10000&max_auto_miles=110000',
    'https://spacecoast.craigslist.org/search/cta?query=honda+civic&purveyor=owner&max_price=10000&max_auto_miles=110000'
]
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; UsedCarFinder; +https://example.com/bot)"
}

def fetch_listings(url):
    print(f"Fetching listings from {url.split('//')[1].split('.')[0]}...")
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code} for URL {url}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    results = []

    for li in soup.select('li.cl-static-search-result'):
        title = li['title']
        link = li.a['href']
        price = li.select_one('.price').text.strip()
        location = li.select_one('.location').text.strip()

        # Visit individual listing and sleep a random amount of seconds between 2-15
        time.sleep(random.uniform(2, 10)) 
        detail_response = requests.get(link, headers=HEADERS)
        if detail_response.status_code != 200:
            print(f"Failed to fetch {link}")
            continue

        detail_soup = BeautifulSoup(detail_response.text, 'html.parser')

        # Extract mileage from the 'odometer' section
        mileage = None
        odometer_section = detail_soup.select_one('.attr.auto_miles .valu')
        if odometer_section:
            mileage = odometer_section.text.strip().replace(',', '')  # Clean it up if necessary
            try:
                mileage = int(mileage)  # Convert to integer if possible
            except ValueError:
                mileage = None

        results.append({
            'title': title,
            'link': link,
            'price': price,
            'location': location,
            'mileage': mileage,
        })

    return results

def main():
    all_cars = []
    for url in urls:
        cars = fetch_listings(url)
        all_cars.extend(cars)

    for car in all_cars:
        print(f"{car['title']} - {car['price']} - Mileage: {car['mileage']}")
        print(f"Link: {car['link']}\n")

if __name__ == "__main__":
    main()

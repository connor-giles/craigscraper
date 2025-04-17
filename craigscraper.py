import re
import requests
from bs4 import BeautifulSoup
import time
import json

# Basic config
url = 'https://orlando.craigslist.org/search/cta?query=honda+civic&purveyor=owner&max_price=10000&max_auto_miles=100000'
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; UsedCarFinder; +https://example.com/bot)"
}
DELAY_BETWEEN_REQUESTS = 2  # seconds

def fetch_listings():
    print("Fetching listings...")
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    results = []

    for li in soup.select('li.cl-static-search-result'):
        title = li['title']
        link = li.a['href']
        price = li.select_one('.price').text.strip()
        location = li.select_one('.location').text.strip()
        mileage = extract_mileage(title)
    
        results.append({
            'title': title,
            'link': link,
            'price': price,
            'location': location,
            'mileage': mileage
        })

    return results

def extract_mileage(title):
    # Look for patterns like "77,000 miles", "77000 mi", "77k", etc.
    match = re.search(r'(\d{1,3}(?:,\d{3})+|\d{4,6})\s*(miles?|mi|k)', title.lower())
    if match:
        mileage_str = match.group(1).replace(',', '')
        if 'k' in mileage_str:
            mileage = int(float(mileage_str.replace('k', '')) * 1000)
        else:
            mileage = int(mileage_str)
        return mileage
    return None

def main():
    cars = fetch_listings()
    for car in cars:
        print(f"{car['title']} - {car['price']}")
        print(f"Link: {car['link']}\n")

if __name__ == "__main__":
    main()

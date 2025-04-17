import requests
from bs4 import BeautifulSoup
import time

# Basic config
BASE_URL = "https://spacecoast.craigslist.org"
SEARCH_URL = BASE_URL + "/search/cta"  # cta = cars+trucks - by all
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; UsedCarFinder; +https://example.com/bot)"
}
DELAY_BETWEEN_REQUESTS = 2  # seconds

def fetch_listings():
    print("Fetching listings...")
    response = requests.get(SEARCH_URL, headers=HEADERS)

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    listings = soup.find_all('li', class_='result-row')
    cars = []

    for listing in listings:
        title_elem = listing.find('a', class_='result-title hdrlnk')
        price_elem = listing.find('span', class_='result-price')
        link = title_elem['href'] if title_elem else None
        title = title_elem.text.strip() if title_elem else 'No title'
        price = price_elem.text.strip() if price_elem else 'No price'

        cars.append({
            'title': title,
            'price': price,
            'link': link
        })

    return cars

def main():
    cars = fetch_listings()
    for car in cars:
        print(f"{car['title']} - {car['price']}")
        print(f"Link: {car['link']}\n")
        time.sleep(DELAY_BETWEEN_REQUESTS)

if __name__ == "__main__":
    main()

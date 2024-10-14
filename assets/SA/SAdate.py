from bs4 import BeautifulSoup
import requests
from datetime import date
import concurrent.futures

current_year = date.today().year

base_url = "https://www.scientificamerican.com/archive/issues/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def scrape_year(year):
    url = f"{base_url}{year}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        issues = soup.select('div[class*=list__item]')

        year_data = []
        for issue in issues:
            link = issue.select_one('a[class*=issue__link]')['href']
            datetime_value = issue.select_one('time')['datetime']
            description = issue.select_one('h3[class*=issue__title]').text

            if "Scientific American" in description:
                full_link = f"https://www.scientificamerican.com{link}"
                year_data.append((datetime_value, description, full_link))
        return year_data
    else:
        print(f"Failed to retrieve the page for {year}. Status code: {response.status_code}")
        return []

data_list = []

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(scrape_year, range(2010, current_year + 2))
    for year_data in results:
        data_list.extend(year_data)

data_list.sort(reverse=True, key=lambda x: x[0])

with open("editiondate.txt", "w", encoding="utf-8") as file:
    for data in data_list:
        file.write(f"{data[0]}\n")

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

current_year = datetime.now().year
start_year = 2024
end_year = current_year + 1

base_url = "https://www.economist.com/weeklyedition/archive?year="

def fetch_dates(year):
    url = f"{base_url}{year}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    dates = []
    links = soup.find_all('a', href=re.compile(r'/weeklyedition/\d{4}-\d{2}-\d{2}'))
    for link in links:
        href = link['href']
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', href)
        if date_match:
            date = date_match.group(0)
            dates.append(date)
    return dates

all_dates = []

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(fetch_dates, year) for year in range(start_year, end_year)]
    for future in as_completed(futures):
        all_dates.extend(future.result())

all_dates.sort(reverse=True)

with open('issuedate_TE.txt', 'w') as file:
    for date in all_dates:
        file.write(date + '\n')

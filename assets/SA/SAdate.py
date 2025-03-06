from bs4 import BeautifulSoup
import requests
from datetime import date
import concurrent.futures

current_year = date.today().year
base_url = "https://www.scientificamerican.com/archive/issues/"
headers = {"User-Agent": "Mozilla/5.0"}

def scrape_year(year):
    url = f"{base_url}{year}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        dates = [issue.select_one('time')['datetime'] 
                 for issue in soup.select('div[class*=list__item]') 
                 if "Scientific American" in issue.select_one('h3[class*=issue__title]').text]
        return dates
    return []

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(scrape_year, range(2010, current_year + 2))
    dates = [date for year_dates in results for date in year_dates]

dates = sorted(set(dates), reverse=True)

with open("editiondate.txt", "w", encoding="utf-8") as file:
    for date in dates:
        file.write(f"{date}\n")
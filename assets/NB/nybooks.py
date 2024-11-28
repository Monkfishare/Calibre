import requests
from bs4 import BeautifulSoup
import re
import datetime

def fetch_dates_for_year(year):
    url = f'https://www.nybooks.com/issues/{year}/'
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    date_pattern = re.compile(rf'https://www.nybooks.com/issues/(\d{{4}}/\d{{2}}/\d{{2}})')
    dates = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        match = date_pattern.search(href)
        if match:
            dates.append(match.group(1))
    dates = list(set(dates))
    dates.sort(reverse=True)
    filename = f'issuedate_NB.txt'
    dates_to_write = dates if year == current_year else dates[1:]
    with open(filename, 'w') as file:
        for date in dates_to_write:
            file.write(date + '\n')
    print(f"Dates for {year} saved to {filename}")

current_year = datetime.datetime.now().year

for year in range(2010, current_year + 1):
    fetch_dates_for_year(year)

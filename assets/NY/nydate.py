import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

url = "https://www.newyorker.com/magazine"
response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, "html.parser")

meta_tag = soup.find("meta", property="og:image")

if meta_tag:
    image_url = meta_tag["content"]
    date_match = re.search(r'/(\d{4}_\d{2}_\d{2})\.', image_url)
    if date_match:
        date_str = date_match.group(1).replace('_', '-')
        issued_date = datetime.strptime(date_str, "%Y-%m-%d")
        formatted_date = issued_date.strftime("%Y/%m/%d")

        with open("issuedate_NY.txt", "w") as file:
            file.write(formatted_date)

        print("Date saved to issuedate_NY.txt:", formatted_date)
    else:
        print("Date not found in the URL.")
else:
    print("Meta tag with property 'og:image' not found.")

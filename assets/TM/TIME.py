import requests
import re
from datetime import datetime

def fetch_issue_ids(start_year, current_year):
    urls = [f"https://time.com/vault/year/{year}/" for year in range(start_year, current_year + 1)]
    issue_ids = []

    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            content = response.text
            pattern = r'"id":(\d+)'
            id_numbers = re.findall(pattern, content)
            if len(id_numbers) > 7:
                id_numbers = id_numbers[7:]

            issue_ids.extend(id_numbers)
        else:
            print(f"Failed to fetch content from {url}. Status code: {response.status_code}")

    issue_ids = list(map(int, issue_ids))
    issue_ids.sort(reverse=True)
    
    with open("issueID_TM.txt", "w", encoding="utf-8") as output_file:
        for id_number in issue_ids:
            output_file.write(str(id_number) + "\n")

    return issue_ids

current_year = datetime.now().year
start_year = current_year - 10
issue_ids = fetch_issue_ids(start_year, current_year)

# print(issue_ids)

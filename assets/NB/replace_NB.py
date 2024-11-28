import datetime
import os

recipe_file = "NB.recipe"
issuedate_file = "issuedate_NB.txt"

if os.path.getsize(issuedate_file) == 0:
    fetch_past_issue_edition = False
else:
    with open(issuedate_file, 'r', encoding='utf-8') as date_file:
        Edition_Date = date_file.readline().strip()

    fetch_past_issue_edition = True

with open(recipe_file, 'r', encoding='utf-8') as file:
    recipe_content = file.read()

modifications = {
    "New York Review of Books (no subscription)": "The New York Review of Books",
    "self.timefmt = text": "self.timefmt = ' [' + text + ']'",
}

if fetch_past_issue_edition:
    modifications['https://www.nybooks.com/current-issue'] = f'https://www.nybooks.com/issues/{Edition_Date}/'

modified_content = recipe_content

for original, replacement in modifications.items():
    modified_content = modified_content.replace(original, replacement)

with open(recipe_file, 'w', encoding='utf-8') as file:
    file.write(modified_content)

if os.path.getsize(issuedate_file) > 0:
    with open(issuedate_file, 'r', encoding='utf-8') as date_file:
        lines = date_file.readlines()

    with open(issuedate_file, 'w', encoding='utf-8') as date_file:
        date_file.writelines(lines[1:])

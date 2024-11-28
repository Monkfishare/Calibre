import os
import re

recipe_file = "NY.recipe"
issuedate_file = "issuedate_NY.txt"
published_date_file = "published_date.txt"

if os.path.getsize(issuedate_file) == 0:
    fetch_past_issue_edition = False
else:
    with open(issuedate_file, 'r', encoding='utf-8') as date_file:
        Edition_Date = date_file.readline().strip()
        with open(published_date_file, 'w', encoding='utf-8') as pub_date_file:
            pub_date_file.write(Edition_Date)
    fetch_past_issue_edition = True

with open(recipe_file, 'r', encoding='utf-8') as file:
    recipe_content = file.read()

recipe_content = re.sub(r"'date'\s*:\s*\{\s*", "'date': {\n            'default': '',\n            ", recipe_content)

modifications = {
    "w_320": "w_1280",
    "w_560": "w_1280",
    "w_640": "w_1600",
}

insert_lines = """
        date_element = soup.select_one('p[class*="BundleHeaderDekText"]')
        if date_element is not None:
            edition_date = date_element.text.strip()
            self.timefmt = ' [' + edition_date + ']'"""

objective_line_pattern = re.compile(r'self\.log\(\'Found cover:\', self\.cover_url\)')
match = objective_line_pattern.search(recipe_content)
if match:
    insert_position = match.end()
    modified_content = recipe_content[:insert_position].rstrip() + insert_lines + recipe_content[insert_position:]
else:
    modified_content = recipe_content

if fetch_past_issue_edition:
    modified_content = re.sub(r"'default': ''", f"'default': '{Edition_Date}'", modified_content)

for original, replacement in modifications.items():
    modified_content = modified_content.replace(original, replacement)

with open(recipe_file, 'w', encoding='utf-8') as file:
    file.write(modified_content)

if os.path.getsize(issuedate_file) > 0:
    with open(issuedate_file, 'r', encoding='utf-8') as date_file:
        lines = date_file.readlines()
    with open(issuedate_file, 'w', encoding='utf-8') as date_file:
        date_file.writelines(lines[1:])

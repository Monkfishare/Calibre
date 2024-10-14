import os
import re

recipe_file = "SA.recipe"
issuedate_file = "editiondate.txt"
edition_info_file = "published_date.txt"

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

recipe_content = read_file(recipe_file)
recipe_content = re.sub(r'\b(800|2000)\b', '', recipe_content)
recipe_content = re.sub(r"'issue_url'\s*:\s*\{\s*", "'issue_url': {\n            'default': '',\n            ", recipe_content)

if os.path.getsize(issuedate_file) > 0:
    issuedate_content = read_file(issuedate_file).splitlines()
    edition_date = issuedate_content[0].strip()
    edition_date_modified = edition_date.replace("-", "/", 1)
    recipe_content = recipe_content.replace(
        "'default': ''", 
        f"'default': 'https://www.scientificamerican.com/issue/sa/{edition_date_modified}/'"
    )
    write_file(recipe_file, recipe_content)
    remaining_lines = issuedate_content[1:]
    write_file(issuedate_file, '\n'.join(remaining_lines) + ('\n' if remaining_lines else ''))
    with open(edition_info_file, 'w', encoding='utf-8') as edition_file:
        edition_file.write(f"{edition_date[:-3]}")

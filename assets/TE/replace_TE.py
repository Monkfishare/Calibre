import os
import re

recipe_file = "TE.recipe"
issuedate_file = "issuedate_TE.txt"

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

recipe_content = read_file(recipe_file)
recipe_content = re.sub(r'\b(600|960|80)\b', '', recipe_content)
# recipe_content = re.sub(r'\bdelay\s*=\s*\d+\b', 'delay = 4', recipe_content)
recipe_content = re.sub(r"format=auto/\'\s*\)", "format=auto/\').replace('SQ_', '')", recipe_content)
recipe_content = re.sub(r"'date'\s*:\s*\{\s*", "'date': {\n            'default': '',\n            ", recipe_content)

if os.path.getsize(issuedate_file) > 0:
    issuedate_content = read_file(issuedate_file).splitlines()
    edition_date = issuedate_content[0].strip()

    recipe_content = re.sub(r"'default': ''", f"'default': '{edition_date}'", recipe_content, count=1)

    remaining_lines = issuedate_content[1:]
    write_file(issuedate_file, '\n'.join(remaining_lines) + ('\n' if remaining_lines else ''))

write_file(recipe_file, recipe_content)

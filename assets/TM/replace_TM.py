recipe_path = "TM.recipe"
issueID_path = "issueID_TM.txt"

try:
    with open(issueID_path, 'r', encoding='utf-8') as file:
        edition_ids = file.readlines()
except FileNotFoundError:
    print("Error: 'issueID_TM.txt' file not found.")
    edition_ids = []

if edition_ids:
    Edition_ID = edition_ids[0].strip()
else:
    Edition_ID = ""

try:
    with open(recipe_path, 'r', encoding='utf-8') as file:
        recipe_content = file.read()
except FileNotFoundError:
    print("Error: 'TM.recipe' file not found.")
    recipe_content = ""

modifications = {
    "self.cover_url = data['hero']['src']['large']": "self.cover_url = data['hero']['src']['large'] + '?quality=100&w=3000'",
    "cover_url = article['hero']['src']['large']": "cover_url = article['hero']['src']['large'] + '?quality=100&w=3000'",
    "img['src'] = img['data-lazy-src']": "img['src'] = img['data-lazy-src'] + '?quality=100&w=1000'",
    "url = article['shortlink']": "url = article['shortlink'].replace('?p=', '')",
    "https://time.com/magazine": f"https://time.com/magazine/us/{Edition_ID}" if Edition_ID else "https://time.com/magazine/us/",
    "['title'].split('|')[0].strip()": "['date']"
}

modified_content = recipe_content
for original, replacement in modifications.items():
    modified_content = modified_content.replace(original, replacement)

try:
    with open(recipe_path, 'w', encoding='utf-8') as file:
        file.write(modified_content)
except FileNotFoundError:
    print("Error: Unable to open 'TM.recipe' for writing.")

remaining_edition_ids = edition_ids[1:]
try:
    with open(issueID_path, 'w', encoding='utf-8') as file:
        file.writelines(remaining_edition_ids)
except FileNotFoundError:
    print("Error: Unable to open 'issueID_TM.txt' for writing.")

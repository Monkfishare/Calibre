import requests
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

def is_url_accessible(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return url, True
    except requests.exceptions.RequestException:
        pass
    return url, False

def generate_issue_dates(start_year=2023):
    urls = []
    current_date = datetime.now() + timedelta(days=30)
    end_date = datetime(year=start_year, month=1, day=1)

    while current_date >= end_date:
        date_str = current_date.strftime('%Y/%m/%d')
        url = f'https://www.newyorker.com/magazine/{date_str}'
        urls.append((date_str, url))
        current_date -= timedelta(days=1)
    
    return urls

def save_successful_dates(dates, filename="issuedate_NY.txt"):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for url in dates:
                date_str = url.split('/')[-3:]
                formatted_date = '/'.join(date_str)
                f.write(f"{formatted_date}\n")
        print(f"Successfully saved {len(dates)} dates to {filename}")
    except IOError as e:
        print(f"Error saving file {filename}: {e}")

def check_urls(urls):
    successful_urls = []

    with ThreadPoolExecutor(max_workers=50) as executor:
        future_to_url = {executor.submit(is_url_accessible, url): url for _, url in urls}
        
        for future in as_completed(future_to_url):
            url, is_accessible = future.result()
            if is_accessible:
                print(f"Success: {url}")
                successful_urls.append(url)
            else:
                print(f"Failed: {url}")
    
    return successful_urls

if __name__ == "__main__":
    urls = generate_issue_dates()
    successful_urls = check_urls(urls)
    successful_urls.sort(reverse=True)
    save_successful_dates(successful_urls)

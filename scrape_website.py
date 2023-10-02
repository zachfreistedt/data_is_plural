### This file is used to populate the data.json file with the most up-to-date information from the Data is Plural archive
### Currently does a full refresh of the file. Plan to edit to check for changed or new editions,
###     and only update/append those records to save time.

from bs4 import BeautifulSoup
import requests
# import lxml
import json
from datetime import datetime

## Functions
def process_link(link):
    link_html = requests.get(link).content
    link_soup = BeautifulSoup(link_html, 'lxml')
    article = link_soup.find('article')

    date_str = article.h2.text[:11].strip()
    date = datetime.strptime(date_str, "%Y.%m.%d").date()  # Parse date string to datetime
    print(date)
    
    summary = article.find('div', class_='edition-summary').text.strip()

    data_dict[date.isoformat()] = {}
    data_dict[date.isoformat()]['Edition Summary'] = summary
    data_dict[date.isoformat()]['Edition Link'] = link
    data_dict[date.isoformat()]['Edition Datasets'] = {}

    edition_body = article.find('div', class_='edition-body')
    edition_ps = edition_body.find_all('p')

    for idx, p in enumerate(edition_ps):
        headline = p.find('strong').text

        first_strong = p.find('strong')
        if first_strong:
            first_strong.extract()

        description = str(p)
        
        links_in_p = [a['href'] for a in p.find_all('a', href=True)]
        data_dict[date.isoformat()]['Edition Datasets'][f'Dataset {idx + 1}'] = {
            'Headline': headline,
            'Description': description,
            'Dataset Links': links_in_p
        }

def get_data():
    url = "https://www.data-is-plural.com/archive/"
    response = requests.get(url) # Send an HTTP GET request to the URL
    html = response.content
    soup = BeautifulSoup(html, "lxml")

    list_el = soup.find('ul', class_='edition-list')
    editions = list_el.find_all('li', class_ = 'edition')

    base_link = 'https://www.data-is-plural.com'

    link_end_list = [edition.find('span', class_='edition-date').find('a')['href'] for edition in editions]
    links_list = [f'{base_link}{link_end[2:]}' for link_end in link_end_list]

    for link in links_list:
        process_link(link)



## Code Execution
data_dict = {}
get_data()

json_data = json.dumps(data_dict, indent=4)
file_path = 'data.json'

# Write JSON data to the file
with open(file_path, 'w') as json_file:
    json_file.write(json_data)
    
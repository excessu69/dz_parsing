import re
import requests
import bs4
from fake_headers import Headers
import time
import json

def get_headers():
    return Headers(os='win', browser='chrome').generate()

response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2',
                        headers=get_headers())
main_html_data = response.text
main_soup = bs4.BeautifulSoup(main_html_data, features='lxml')

tag_div_vacancy_lit = main_soup.find('main',class_='vacancy-serp-content')
vacancy_tags = tag_div_vacancy_lit.find_all('div', class_='serp-item')

parsed_data = []

for vacancy_tag in vacancy_tags:
    h2_tag = vacancy_tag.find('span', class_='serp-item__title-link-wrapper')
    a_tag = h2_tag.find('a')
    absolute_link = a_tag['href']
    title = h2_tag.text

    time.sleep(0.3)
    vacancy_response = requests.get(absolute_link, headers=get_headers())
    vacancy_html_data = vacancy_response.text
    vacancy_soup = bs4.BeautifulSoup(vacancy_html_data, features='lxml')


    description_tag = vacancy_soup.find('div', class_='vacancy-description')
    if description_tag:
        description = description_tag.text.lower()
    else:
        description = ""


    if 'django' in description and 'flask' in description:
        match = re.search(r'(.+?\.)', description)
        if match:
            parsed_data.append({
                'title': title,
                'link': absolute_link,
                'description': match.group()
            })


with open('vacancies.json', 'w', encoding='utf-8') as f:
    json.dump(parsed_data, f, ensure_ascii=False, indent=4)






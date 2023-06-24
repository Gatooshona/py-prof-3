import json
import re
import requests
import fake_headers
from bs4 import BeautifulSoup


headers = fake_headers.Headers(browser='firefox', os='win')
headers_dict = headers.generate()

main_html = requests.get(
    'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'.strip(),
    headers=headers_dict).text
main_soup = BeautifulSoup(main_html, 'lxml')

div_job_list_tag = main_soup.find('div', id='a11y-main-content')  # все вакансии на странице
job_item = div_job_list_tag.find_all('div', class_='vacancy-serp-item-body__main-info')

data = []

for job in job_item:
    h3_tag = job.find('h3')
    title = h3_tag.text
    a_tag = h3_tag.find('a')
    link = a_tag['href']
    company_name = job.find('div', class_='vacancy-serp-item__meta-info-company').text
    city = job.find('div', class_='vacancy-serp-item-company').find_all('div',
                                                                        class_='bloko-text')[1].text.split()[0]
    salary = job.find('span', class_='bloko-header-section-3')

    if salary:
        salary = salary.text
    else:
        salary = '-'

    job_html = requests.get(link, headers=headers.generate()).text
    html_soup = BeautifulSoup(job_html, 'lxml')
    job_all_info = html_soup.find('div', class_='bloko-tag-list')

    if job_all_info:
        if job_all_info.find(string=re.compile('Django.')) or job_all_info.find(string='Flask.'):
            data.append({
                'title': title,
                'link': link,
                'salary': salary,
                'company': company_name,
                'city': city
            })

with open('data.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

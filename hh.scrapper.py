from bs4 import BeautifulSoup as bs
import requests
import re
from pprint import pprint

# https://hh.ru/search/vacancy?text=Python
url = 'https://hh.ru'

item = input('Введите поисковый запрос для hh.ru\n')
page_number = 0

params = {'text': item, 'page': page_number}
headers = {f'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}



# функция, отвечающая за сбор данных
def scrapping_page():
    response = requests.get(url + '/search/vacancy', params=params, headers=headers)
    soup = bs(response.content.decode('utf-8'), 'html.parser')
    vacancy_list = soup.find_all('div', {'class': 'vacancy-serp-item'})

    for vacancy in vacancy_list:
        vacancy_data = {}

        try:
            vacancy_name = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).getText()
        except AttributeError:
            vacancy_name = None

        try:
            vacancy_url = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).get('href')
        except AttributeError:
            vacancy_url = None

        try:
            vacancy_adress = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-address'}).getText()
        except AttributeError:
            vacancy_adress = None

        try:
            vacancy_compensation = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).getText()
        except AttributeError:
            vacancy_compensation = None

        if vacancy_compensation == 'з/п не указана':
            vacancy_compensation = None

        if vacancy_compensation:
            vacancy_compensation = vacancy_compensation.replace('\u202f', '')
            vacancy_compensation = vacancy_compensation.replace('от ', '')
            vacancy_compensation = vacancy_compensation.replace('на руки', '')
            vacancy_compensation = vacancy_compensation.replace('до', '-')
            vacancy_compensation = re.split(r'\s|-', vacancy_compensation)
            compensation_min = vacancy_compensation[0]

            try:
                compensation_max = vacancy_compensation[2]
            except IndexError:
                compensation_max = None
            try:
                compensation_currency = vacancy_compensation[-1]
            except IndexError:
                compensation_currency = None
        if vacancy_compensation is None:
            compensation_min = None
            compensation_max = None
            compensation_currency = None
        vacancy_data['Ссылка'] = vacancy_url
        vacancy_data['Адрес'] = vacancy_adress
        vacancy_data['Минимальная з/п'] = compensation_min
        vacancy_data['Максимальная з/п'] = compensation_max
        vacancy_data['Валюта'] = compensation_currency
        vacancy_data['Вакансия'] = vacancy_name

        pprint(vacancy_data)


enumenator = True  # переменная, отвечающая за цикл собирающий данные

while enumenator: # сам цикл

    scrapping_page()
    try:
        enumenator = bs(requests.get(url + '/search/vacancy', params=params, headers=headers).text, 'html.parser') \
                         .find('a', {'data-qa': 'pager-next'}).getText() == 'дальше'
    except AttributeError:
        enumenator = False
    page_number += 1
    params = {'text': item, 'page': page_number}


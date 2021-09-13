from pymongo import MongoClient
from bs4 import BeautifulSoup as bs
import requests
import re
from pprint import pprint

item = input('Введите поисковый запрос для hh.ru\n')
zp = int(input('Введите минимальную з/п\n'))

# https://hh.ru/search/vacancy?text=Python
url = 'https://hh.ru'
page_number=0
params = {'text': item, 'page': page_number}
headers = {f'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}

client = MongoClient('localhost', 27017)
db = client['dz_database']
hh = db['hh']


# функция, записывающая данные в монго
def all_data_to_mongo(page_number, params):
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
                try:
                    compensation_min = int(vacancy_compensation[0])
                except  ValueError:
                    compensation_min = None
                try:
                    compensation_max = int(vacancy_compensation[2])
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
            result = hh.insert_one(vacancy_data)
            pprint(result)

    enumenator = True  # переменная, отвечающая за цикл собирающий данные

    while enumenator:  # сам цикл

        scrapping_page()
        try:
            enumenator = bs(requests.get(url + '/search/vacancy', params=params, headers=headers).text, 'html.parser') \
                             .find('a', {'data-qa': 'pager-next'}).getText() == 'дальше'
        except AttributeError:
            enumenator = False
        page_number += 1
        params = {'text': item, 'page': page_number}


# функция, выводящая все вакансии с минимальной зп выше указанной
def show_vacancy(compensation):
    for el in hh.find({'Минимальная з/п': {'$gt': compensation}}):
        pprint(el)

#функция, дописывающая в бд новые вакансии
def new_vacancy(page_number, params):
    def update_db():
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
                try:
                    compensation_min = int(vacancy_compensation[0])
                except  ValueError:
                    compensation_min = None
                try:
                    compensation_max = int(vacancy_compensation[2])
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
            result = hh.update_one(vacancy_data)
            pprint(result)


all_data_to_mongo(page_number, params)
show_vacancy(zp)
new_vacancy(page_number, params)
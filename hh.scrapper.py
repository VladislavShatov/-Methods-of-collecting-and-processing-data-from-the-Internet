from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

# https://hh.ru/search/vacancy?text=Python
url = 'https://hh.ru'

item = input('Введите поисковый запрос для hh.ru\n')
page_number = 0

params = {'text': item, 'page': page_number}
headers = {f'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}


# создаём счетчик
def counter():
    i = 0

    def func():
        nonlocal i
        i += 1
        return i

    return func


# функция, отвечающая за сбор данных
def scrapping_page():
    response = requests.get(url + '/search/vacancy', params=params, headers=headers)
    soup = bs(response.text, 'html.parser')
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

        vacancy_data['Ссылка'] = vacancy_url
        vacancy_data['Адрес'] = vacancy_adress
        vacancy_data['З/п'] = vacancy_compensation
        vacancy_data['Вакансия'] = vacancy_name
        counter()

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

print(counter() - 1)

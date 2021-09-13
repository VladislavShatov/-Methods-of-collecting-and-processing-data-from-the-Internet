from lxml import html
import requests
from pymongo import MongoClient
from pprint import pprint


client = MongoClient('localhost', 27017)
db = client['dz']
news_mail_ru = db['news_mail_ru']
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
response = requests.get('https://news.mail.ru/', headers=header)
dom = html.fromstring(response.text)
text = dom.xpath("//ul[contains(@class,'list list_type_square list_half js-module')]//li//a/text()")
text_list = []
news_list = {}
a = 0
for el in text:
    el = el.replace('\xa0',' ')
    text_list.append(el)
links_list = dom.xpath("//ul[contains(@class,'list list_type_square list_half js-module')]//li//a/@href")
while a != len(text_list):
    news_list['_id'] = a
    news_list['Новость'] = text_list[a]
    news_list['Источник'] = 'news.mail.ru'
    news_list['Ссылка'] = links_list[a]
    a+=1
    pprint(news_list)
    result = news_mail_ru.insert_one(news_list)
print(result)
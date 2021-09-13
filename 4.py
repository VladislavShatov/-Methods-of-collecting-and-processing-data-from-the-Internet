from lxml import html
import requests
from pprint import pprint

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
response = requests.get('https://news.mail.ru/', headers=header)
dom = html.fromstring(response.text)
text = dom.xpath("//ul[contains(@class,'list list_type_square list_half js-module')]//li//a/text()")
text_list = []
news_list = []
print('Источник новостей - news.mail.ru')
for el in text:
    el = el.replace('\xa0',' ')
    text_list.append(el)
links_list = dom.xpath("//ul[contains(@class,'list list_type_square list_half js-module')]//li//a/@href")
a = 0
while a != len(text_list):
    news_list.append(text_list[a])
    news_list.append(links_list[a])
    a+=1
pprint(news_list)
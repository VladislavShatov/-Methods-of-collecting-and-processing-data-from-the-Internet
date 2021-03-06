from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leruaparser.spiders.lerua import LeruaSpider
from leruaparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    answer = input('Введите поисковый запрос\n')
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeruaSpider, search=answer)
    process.start()
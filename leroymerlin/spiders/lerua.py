import scrapy
from scrapy.http import HtmlResponse
from leruaparser.items import LeruaparserItem
from scrapy.loader import ItemLoader

class LeruaSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        super().__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']


    def parse(self, response:HtmlResponse):
        ads_links = response.xpath("//a[@data-qa='product-image']//@href")
        for link in ads_links:
            yield response.follow(link, callback=self.ads_parse)

    def ads_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=LeruaparserItem(), response=response)
        loader.add_value('url', response.url)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//uc-pdp-price-view[@slot='primary-price']/span[@slot='price']/text()")
        loader.add_xpath('photos', "//picture[@slot='pictures']/img[@itemprop='image']/@src")

        yield loader.load_item()
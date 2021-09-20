import scrapy
from scrapy.http import HtmlResponse

from bookparser.items import BookparserItem


class Labirint(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/rating/']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//span[@class='product-title']/parent::*/@href").extract()
        next_page = response.xpath("//div[@class='pagination-next']//@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        for link in links:
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):

        price_data = response.xpath("//span[@class='buying-priceold-val-number']/text()").extract_first()
        link_data = str(response.url)
        try:
            data = response.xpath("//h1/text()").extract_first().split(':', 1)
            name_data = data[1]
            author_data = data[0]
        except IndexError:
            name_data = response.xpath("//h1/text()").extract_first()
            author_data = None
        sale_data = response.xpath("//span[@class='buying-pricenew-val-number']/text()").extract_first()
        rating_data = response.xpath("//div[@id='rate']/text()").extract_first()
        yield BookparserItem(name=name_data, price=price_data, link=link_data, author=author_data, sale=sale_data,
                             rating=rating_data)

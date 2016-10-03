import scrapy
from scrapy.selector import Selector
from tutorial.items import MyItem
from scrapy.http import Request

class MySpider(scrapy.Spider):
    name = "ewg"
    start_urls = [
        "http://www.ewg.org/skindeep/browse/tanning+oil/",
    ]
    url = "http://www.ewg.org"

    def parse(self, response):
        table = Selector(response).xpath('//*[@id="table-browse"]/tbody/tr')[1:]

        for row in table:
            item = MyItem()
            item['img_url'] = row.xpath('td[2]/a/img/@src').extract()
            item['title'] = row.xpath('td[3]/a/text()').extract()
            content_url = row.xpath('td[3]/a/@href').extract_first()
            yield Request(self.url + content_url, callback=self.parse_content, meta={'item': item})

        next_link = response.xpath('//*[@id="click_next_number"]/a[contains(text(),"Next")]/@href').extract_first()

        if next_link:
            yield Request(self.url + next_link, callback=self.parse)

    def parse_content(self, response):
        item = response.meta["item"]
        item['ingredients'] = response.xpath('//*[@id="Ingredients"]/table//tr/td[1]/a/text()').extract()
        yield item


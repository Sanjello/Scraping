import scrapy
from ScrapEkUa.items import ScrapekuaItem


class WashingSpider(scrapy.Spider):
    name = 'Washing'
    start_urls = ['https://ek.ua/ua/list/91/']
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'Mashines.json'
    }
    def parse(self, response):
        model = response.css("td.model-short-info table tr td a span.u::text").extract()
        characteristic_item = response.css("div.model-short-description div.m-s-f2 ")
        characteristic = []

        for i in range(len(model)):
            characteristic.append({})
            c =characteristic_item[i]
            for j in range(len(c.css('div.m-s-f2 span::text').extract())):
                characteristic[i][c.css('div.m-s-f2 span::text').extract()[j]]=\
                    c.css('div.m-s-f2 div::text').extract()[j].replace("\xa0"," ")

        for i in range(len(model)):
            item = ScrapekuaItem()
            item["model"] = model[i]
            item["characteristic"] = characteristic[i]
            yield item
        next_page = response.css("div.list-pager a#pager_next::attr('href')").extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)


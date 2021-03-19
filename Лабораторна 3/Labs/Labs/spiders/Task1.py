import scrapy
from Labs.items import LabsItem


class Task1Spider(scrapy.Spider):
    name = 'Task1'
    allowed_domains = ['hotline.ua']
    start_urls = ['https://hotline.ua/mobile/mobilnye-telefony-i-smartfony']

    def parse(self, response):
        item_model = response.css("div.item-info p.h4 a::text").getall()
        item_price = response.css("div.price-md span.value::text").getall()
        item_more = response.css("div.item-price div.stick-pull a.link::text ").getall()

        # Some string transformation
        for i in range(len(item_model)):
            item_model[i] = item_model[i].replace("\n", "")
            item_price[i] = item_price[i].replace("\u00a0", "")
            len_of_more = len(item_more[i])
            item_more[i] = (item_more[i][len_of_more - 4:len_of_more - 1:]).replace("(", "")
            item_more[i] = item_more[i].replace("\u00a0", "")
            if item_more[i].isdigit():
                item_more[i] = int(item_more[i])
            else:
                item_more[i] = 0
        # Form result
        for i in range(len(item_model)):
            hot_item = LabsItem()
            hot_item["name"] = item_model[i]
            hot_item["price"] = float(item_price[i])
            hot_item["more"] = item_more[i]
            yield hot_item
        # Check and go to the next page
        next_page = response.css("a.next::attr('href')").extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

import scrapy


# Spider for parsing Mobile Phones from Hotline
class HotlineMobileScrapper(scrapy.Spider):

    # Some parameters of spider
    name = "HotSp"
    allowed_domains = ['hotline.ua']
    start_urls = ['https://hotline.ua/mobile/mobilnye-telefony-i-smartfony']
    custom_settings = {
        'FEED_FORMAT': 'jsonlines',
        'FEED_URI': 'Smartfones.jl'
    }

    def parse(self, response):
        item_model = response.css("div.item-info p.h4 a::text").extract()
        item_price = response.css("div.price-md span.value::text").extract()
        item_more = response.css("div.item-price div.stick-pull a.link::text ").extract()

        # Some string transformation
        for i in range(len(item_model)):
            item_model[i] = item_model[i].replace("\n", "")
            item_price[i] = item_price[i].replace("\u00a0", "")
            len_of_more = len(item_more[i])
            item_more[i] = (item_more[i][len_of_more - 4:len_of_more - 1:]).replace("(", "")
            item_more[i] = item_more[i].replace("\u00a0", "")

        # Form result
        for i in range(len(item_model)):
            yield {
                'Model': item_model[i],
                'Price': item_price[i],
                'More': item_more[i]
            }
        # Check and go to the next page
        next_page = response.css("a.next::attr('href')").extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

import scrapy


# Spider for parsing Mobile Phones from Hotline
class SienceSpider(scrapy.Spider):
    # Some parameters of spider
    name = "SienceSpider"
    start_urls = [
        'http://www.irbis-nbuv.gov.ua/cgi-bin/irbis_nbuv/cgiirbis_64.exe?S21CNR=1000&S21STN=1&S21REF=2&C21COM=S&I21DBN'
        '=UJRN&P21DBN=UJRN&S21All=%3C.%3EDP=2020$%3C.%3E&S21FMT=fullwebr&Z21ID=']

    def parse(self, response):
        start_url = 'http://www.irbis-nbuv.gov.ua'
        book_url = []
        book_name = []
        block = response.css('table.advanced tr td table').getall()
        for item in block:
            url = self.start_url + item.css("tr td a img::attr('src')").get()
            name = item.css("tr td p[0]::text").get()
            print(url,name)

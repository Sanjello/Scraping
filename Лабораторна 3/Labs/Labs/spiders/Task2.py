import scrapy
from Labs.items import BookItem


class Task2Spider(scrapy.Spider):
    name = 'Task2'
    start_urls = [
        'http://www.irbis-nbuv.gov.ua/cgi-bin/irbis_nbuv/cgiirbis_64.exe?S21CNR=1000&S21STN=1&S21REF=2&C21COM=S&I21DBN'
        '=UJRN&P21DBN=UJRN&S21All=%3C.%3EDP=2020$%3C.%3E&S21FMT=fullwebr&Z21ID=']

    def parse(self, response):
        start_url = 'http://www.irbis-nbuv.gov.ua'
        book_image = response.css("table tr td table tr td table a img::attr('src')").extract()
        book_name = []
        for b in response.css("table.advanced tr td table tr td p"):
            name = b.css("::text").extract_first()
            if name != None and name != "Додаткові відомості та надходження":
                book_name.append(b.css("::text").extract_first())
        for i in range(len(book_image)):
            book_image[i] = start_url + book_image[i]
        for i in range(len(book_image)):
            book = BookItem()
            book["url"] = book_image[i]
            book["name"] = book_name[i]
            yield book

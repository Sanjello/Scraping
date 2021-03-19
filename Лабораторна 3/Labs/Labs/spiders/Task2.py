import scrapy
from Labs.items import BookItem


class Task2Spider(scrapy.Spider):
    name = 'Task2'
    start_urls = [
        'http://www.irbis-nbuv.gov.ua/cgi-bin/irbis_nbuv/cgiirbis_64.exe?S21CNR=1000&S21STN=1&S21REF=2&C21COM=S&I21DBN'
        '=UJRN&P21DBN=UJRN&S21All=%3C.%3EDP=2020$%3C.%3E&S21FMT=fullwebr&Z21ID=']

    def parse(self, response):
        start_url = 'http://www.irbis-nbuv.gov.ua'
        book_url = []
        book_name = []
        block = response.css('table.advanced tr td table')
        for item in block:
            book_url.append(item.css("tr td a img::attr('src')").get())
            book_name.append(item.css("tr td p::text").get())
        for i in range(len(book_url)):
            if book_url[i] !=None:
                book_url[i] = start_url + book_url[i]
            else:pass
        for i in range(len(book_url)):
            book = BookItem()
            book["url"] = book_url[i]
            book["name"] = book_name[i]
            yield book

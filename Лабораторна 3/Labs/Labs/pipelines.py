# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from itemadapter import ItemAdapter
from sqlite3 import connect
from scrapy.exceptions import DropItem

class Task1Pipeline:
    def open_spider(self, spider):
        self.number = 0

    def process_item(self, item, spider):
        return item

    def close_spider(self, spider):
        print("=" * 50)
        print(f"{self.number} items have been processed")

class SqlPipeline:

    def open_spider(self, spider):
        if spider.name == 'Task1':
            self.connection = connect('..\Hotline.db')
        elif spider.name == 'Task2':
            self.connection = connect('..\Sience.db')
        else:pass


    def process_item(self, item, spider):
        if spider.name == 'Task1':
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO Smartphones (Name,Price,More) VALUES (?, ?, ?)", [item["name"],  item ["price"], item["more"]])
            self.connection.commit()
            return item
        elif spider.name =='Task2':
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO Books (url,Name) VALUES (?, ?)",
                           [item["url"], item["name"]])
            self.connection.commit()
            return item
        else:pass


    def close_spider(self, spider):
        self.connection.close()


class DuplicateFilterPipeline:

    def open_spider(self, spider):
        if spider.name == 'Task1':
            self.connection = connect('..\Hotline.db')
        elif spider.name == 'Task2':
            self.connection = connect('..\Sience.db')
        else:pass

    def process_item(self, item, spider):
        if spider.name == 'Task1':
            cursor = self.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM Smartphones WHERE Name = ?", [item["name"]])
            if cursor.fetchone()[0] > 0:
                raise DropItem(f"Duplicate {item['name']}")
            return item
        elif spider.name == 'Task2':
            cursor = self.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM Books WHERE Name = ?", [item["name"]])
            if cursor.fetchone()[0] > 0:
                raise DropItem(f"Duplicate {item['name']}")
            return item

    def close_spider(self, spider):
        self.connection.close()

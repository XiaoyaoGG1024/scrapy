# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from itemadapter import ItemAdapter
import openpyxl


# 数据库

# CREATE TABLE `top250` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `title` varchar(50) NOT NULL,
#   `score` varchar(5) NOT NULL,
#   `comment` varchar(100) DEFAULT NULL,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
class dbPipeline:
    def __init__(self):
        HOST = 'localhost'
        PORT = 3306
        USER = 'root'
        PASSWORD = '123456'
        DATABASE = 'test'
        CHARSET = 'utf8'
        self.conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database=DATABASE,
                                    charset=CHARSET)
        self.cursor = self.conn.cursor()
        self.data = []

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        #批处理
        if len(self.data) > 0:
            self.writeToDb()
        self.conn.close()

    def writeToDb(self):
        self.cursor.executemany("insert into top250(title,score,comment) values(%s,%s,%s);", self.data)
        self.conn.commit()

    def process_item(self, item, spider):
        title = item.get('title', '')
        score = item.get('score', 0)
        comment = item.get('comment', '')
        self.data.append((title, score, comment))
        #批处理
        if len(self.data) == 100:
            self.writeToDb()
            self.data.clear()
        return item


# 通道与设置表对应
class excelPipeline:
    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        # sheet
        self.ws.title = 'Top250'
        # 列
        self.ws.append(('title', 'score', 'comment'))

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.wb.save('top250.xlsx')

    def process_item(self, item, spider):
        title = item.get('title', '')
        score = item.get('score', '')
        comment = item.get('comment', '')
        self.ws.append((title, score, comment))
        return item

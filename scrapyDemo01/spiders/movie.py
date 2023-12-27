import re

import scrapy
from scrapy import Selector, Request
from ..items import MovieItem


class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['movie.douban.com']

    def start_requests(self):
        for page in range(1):
            yield Request(url=f'http://movie.douban.com/top250?start={page * 25}&filter=')

    def parse(self, response, **kwargs):
        sel = Selector(response)
        # content > div > div.article > ol > li:nth-child(1)
        list_items = sel.css('#content > div > div.article > ol > li')
        # 创建 movie_item对象
        movie_item = MovieItem()
        for item in list_items:
            # content > div > div.article > ol > li:nth-child(1) > div > div.info > div.hd > a
            movie_Detail_Url = item.css('div.info > div.hd > a::attr(href)').extract_first()
            print(movie_Detail_Url)
            # < span>class ="title" > 肖申克的救赎 < / span >
            movie_item['title'] = item.css('span.title::text').extract_first()
            movie_item['score'] = item.css('span.rating_num::text').extract_first()
            movie_item['comment'] = item.css('span.inq::text').extract_first() or '该电影没有描述哦'
            # 解析子页面
            yield Request(url=movie_Detail_Url,
                          callback=self.url_parse,
                          cb_kwargs={'item': movie_item}
                          )

    def url_parse(self, response, **kwargs):
        movie_item = kwargs['item']
        sel = Selector(response)
        # info > span:nth-child(1) > span.attrs > a
        movie_item['actors'] = sel.css('span.attrs > a::text').extract_first()
        yield movie_item

    # def parse(self, response):
    #     # 创建 movie_item对象
    #     movie_item = MovieItem()
    #     #// *[ @ id = "content"] / div / div[1] / ol / li[1]
    #     list_items = response.xpath('//*[@id="content"]/div/div[1]/ol/li')  # 总的
    #     for list_item in list_items:
    #         #// *[ @ id = "content"] / div / div[1] / ol / li[1] / div / div[2] / div[1] / a / span[1]
    #         movie_item['title'] = list_item.xpath('./div/div[2]/div[1]/a/span[1]/text()').get()  # 使用键值
    #         movie_item['score'] = list_item.xpath('./div/div[2]/div[2]/div/span[2]/text()').get()
    #         movie_item['comment'] = list_item.xpath('./div/div[2]/div[2]/p[2]/span/text()').get()
    #         #// *[ @ id = "content"] / div / div[1] / ol / li[1] / div / div[2] / div[1] / span
    #         movie_item['playable']= list_item.xpath('./div/div[2]/div[1]/span/text()').get()
    #         yield movie_item
    #     #获取页面数据
    #     data=response.text
    #     directors = re.findall(r'.*导演: (.*?)&nbsp;&nbsp;&nbsp;主演', data)
    #     actors = re.findall(r'.*导演: .*?&nbsp;&nbsp;&nbsp;主演: (.*?)<br>', data)
    #     year = re.findall(r'.*(\d{4})&nbsp;/&nbsp;.*', data)
    #     country = re.findall(r'.*\d{4}&nbsp;/&nbsp;(.*)&nbsp;/&nbsp;', data)
    #     genre = re.findall(r'.*\d{4}&nbsp;/&nbsp;.*&nbsp;/&nbsp;(.*)', data)
    #     for i in range(0, len(directors)):
    #         movie_item['director'] = directors if directors[i] else None
    #         movie_item['actor'] = actors if actors[i] else None
    #         movie_item['year'] = year if  year[i]else None
    #         movie_item['country'] = country if country[i] else None
    #         movie_item['genre'] = genre if genre[i] else None
    #         yield movie_item

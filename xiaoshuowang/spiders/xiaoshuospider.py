# -*- coding: utf-8 -*-
import scrapy
from xiaoshuowang.items import XiaoshuowangItem
import sys
import os

# 设定默认encoding为utf-8
reload(sys)
sys.setdefaultencoding("utf-8")


class XiaoshuospiderSpider(scrapy.Spider):
    name = 'xiaoshuospider'
    allowed_domains = ['x23us.com']
    # 构造起始url
    offset = 1
    url = "https://www.x23us.com/quanben/"
    start_urls = [url + str(offset)]

    def parse(self, response):
        items = []
        # 匹配书名
        bookname = response.xpath("//tr/td[@class='L']/a[2]/text()").extract()
        # 匹配书名链接
        booknameLink = response.xpath("//tr/td[@class='L']/a[2]/@href").extract()

        # 循环爬取所有书名
        for i in range(0, len(bookname)):
            # 实例化item
            item = XiaoshuowangItem()

            # 保存书名和链接
            item["bookname"] = bookname[i]
            item["booknameLink"] = booknameLink[i]

            # 指定书本存放路径
            bookFilename = "./book/" + bookname[i]

            # 如果目录不存在则创建目录
            if (not os.path.exists(bookFilename)):
                os.makedirs(bookFilename)

            # 保存书本存放路径
            item["bookFilename"] = bookFilename

            # 将数据保存到items，以便传输到下个parser
            items.append(item)


        # 将每本书url的Request请求，以及response中的meta数据，一起提交至title_parser方法
        for item in items:
            yield scrapy.Request(item["booknameLink"], meta={"meta_1": item}, callback=self.title_parse)

        # 翻页在提取书本url
        if self.offset < 1:
            self.offset += 1

            yield scrapy.Request(self.url + str(self.offset), callback=self.parse)

    # 返回的书本url，再进行递归解析和请求
    def title_parse(self, response):
        # 提起上一步骤的response中的meta数据
        meta_1 = response.meta["meta_1"]

        # 提取章节名和链接
        title = response.xpath("//tr/td[@class='L']/a/text()").extract()
        titleLink = response.xpath("//tr/td[@class='L']/a/@href").extract()

        items = []

        for i in range(0, len(titleLink)):
            # 实例化item
            item = XiaoshuowangItem()

            # 保存上个response和这个response的值
            item["bookname"] = meta_1["bookname"]
            item["booknameLink"] = meta_1["booknameLink"]
            item["bookFilename"] = meta_1["bookFilename"]
            item["title"] = title[i]
            item["titleLink"] = meta_1["booknameLink"] + titleLink[i]
            # item["titleLink"] = 'https://www.x23us.com/html/64/64231/26135744.html'

            # 存入items，以便传输至下个parse
            items.append(item)

        for item in items:
            yield scrapy.Request(item["titleLink"], meta={"meta_2": item}, callback=self.contents_parse)

    def contents_parse(self, response):
        item = response.meta["meta_2"]


        contents = ""

        contents_list = response.xpath("//dd[@id='contents']/text()").extract()

        for content in contents_list:
            contents += content

        item["contents"] = contents

        yield item

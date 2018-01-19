# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

class XiaoshuowangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #书名
    bookname = scrapy.Field()
    #书名链接
    booknameLink = scrapy.Field()
    #书本路径
    bookFilename = scrapy.Field()
    #章节名
    title = scrapy.Field()
    #章节链接
    titleLink =scrapy.Field()
    #内容
    contents = scrapy.Field()


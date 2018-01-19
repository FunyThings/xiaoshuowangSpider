# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

class XiaoshuowangPipeline(object):
    def process_item(self, item, spider):

        filename = item["title"].replace("/","_")
        filename += ".txt"

        fp = open(item["bookFilename"] + "/" + filename , "w")
        fp.write(item["contents"])
        fp.close()

        return item

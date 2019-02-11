# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import requests

class MeinrPipeline(object):
    def open_spider(self,spider):
        self.path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep + 'download'
        # print(self.path)
    def process_item(self, item, spider):
        title = item['title']
        img = item['img']
        num = item['num']
        path = self.path + os.sep + title
        if not os.path.exists(path):
            os.makedirs(path)
        html = requests.get(url=img,headers=spider.headers).content
        path = path + os.sep + str(num) + '.jpg'
        with open(path,'wb')as f:
            f.write(html)
        return item

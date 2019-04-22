# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
"""
源码内容：
    1.判断当前XdbPipeline类中是否有from_crawler
        有：
            obj = XdbPipeline.from_crawler(.....)
        否:
            obj = XdbPipeline()
    2. obj.open_spider()
    3. obj.process_item()/process_item()/process_item()
    4. obj.close_spider()
"""


class ScrapyxdbPipeline(object):
    def __init__(self,path):
        self.f = None
        self.path = path

    @classmethod  # 不需要实例化 直接类名.方法
    def from_crawler(cls, crawler):
        """
        初始化时候，用于创建pipeline对象
        :param crawler:
        :return:
        """
        print('File.from_crawler')
        path = crawler.settings.get('HREF_FILE_PATH')
        return cls(path)

    def open_spider(self, spider):
        """
        爬虫开始执行时，调用
        :param spider:
        :return:
        """
        self.f = open(self.path,'a+',encoding='utf-8')
        print('爬虫开始')

    def process_item(self, item, spider):
        print('pipelines',item)
        self.f.write(item['title']+item['up']+item['watch'].strip()+'\n')
        return item

    def close_spider(self, spider):
        """
        爬虫关闭时，被调用
        :param spider:
        :return:
        """
        self.f.close()
        print('爬虫结束')

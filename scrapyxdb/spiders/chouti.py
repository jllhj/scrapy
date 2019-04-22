# -*- coding: utf-8 -*-
import scrapy
from scrapyxdb.items import ScrapyxdbItem


class ChoutiSpider(scrapy.Spider):
    name = 'chouti'
    allowed_domains = ['bilibili.com']
    start_urls = ['https://search.bilibili.com/all?keyword=%E8%94%A1%E5%BE%90%E5%9D%A4&from_source=banner_search&order=click&duration=0&tids_1=0&page=1']

    def parse(self, response):
        video_list = response.xpath('//*[@id="server-search-app"]/div[2]/div[2]/div/div[2]/ul/li[@class="video matrix"]')
        # f = open('content.txt', 'a+', encoding='utf-8')
        for video in video_list:
            title = video.xpath('.//a[@class="title"]/@title').extract_first()
            # print(title)
            up = video.xpath('.//a[@class="up-name"]/text()').extract_first()
            watch = video.xpath('.//span[@class="so-icon watch-num"]/text()').extract_first()
            print(up,watch)
            yield ScrapyxdbItem(title=title,up=up,watch=watch)
        #     f.write('标题： '+title+'  UP主： '+up+'  播放量：'+watch.strip()+'\n')
        #
        # f.close()

        # page_list = ['https://search.bilibili.com/all?keyword=%E8%94%A1%E5%BE%90%E5%9D%A4&from_source=banner_search&order=click&duration=0&tids_1=0&page={0}'.format(i) for i in range(2,51)]
        # for page in page_list:
        #     from scrapy.http import Request
        #     yield Request(url=page,callback=self.parse)
# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider,Request
import json
from ..items import UserItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    start_user = 'excited-vczh'

    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_include = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'

    # 关注人
    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follows_include = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    # 粉丝
    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    followers_include = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        # url = 'https://www.zhihu.com/api/v4/members/binka?include=allow_message%2Cis_followed%2Cis_following%2Cis_org%2Cis_blocking%2Cemployments%2Canswer_count%2Cfollower_count%2Carticles_count%2Cgender%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'
        # url = 'https://www.zhihu.com/api/v4/members/excited-vczh/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=40&limit=20'
        yield Request(self.user_url.format(user=self.start_user,include=self.user_include),callback=self.parse_user)
        yield Request(self.follows_url.format(user=self.start_user,include=self.follows_include,offset=0,limit=20),callback=self.parse_follows)
        yield Request(self.followers_url.format(user=self.start_user, include=self.followers_include, offset=0, limit=20),
                      callback=self.parse_followers)

    def parse_user(self, response):
        result = json.loads(response.text)
        item = UserItem()

        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        # print(item)
        yield item

        # 获取每一个的关注列表
        yield Request(self.follows_url.format(user=result.get('url_token'),include=self.follows_include,limit=20,offset=0),self.parse_follows)
        # 粉丝
        yield Request(
            self.followers_url.format(user=result.get('url_token'), include=self.followers_include, limit=20, offset=0),
            self.parse_follows)

    def parse_follows(self, response):
        results = json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                yield  Request(self.user_url.format(user=result.get('url_token'),include=self.user_include),self.parse_user)

        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page_offset = results.get('paging').get('next').rsplit('offset=',1)[1]
            next_page = self.follows_url.format(user=self.start_user,include=self.follows_include,offset=next_page_offset,limit=20)
            yield Request(next_page,self.parse_follows)

    def parse_followers(self, response):
        results = json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                yield  Request(self.user_url.format(user=result.get('url_token'),include=self.user_include),self.parse_user)

        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page_offset = results.get('paging').get('next').rsplit('offset=',1)[1]
            next_page = self.follows_url.format(user=self.start_user,include=self.follows_include,offset=next_page_offset,limit=20)
            yield Request(next_page,self.parse_followers)
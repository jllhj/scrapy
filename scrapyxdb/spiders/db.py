# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.cookies import CookieJar
from scrapy.http import Request
from urllib.parse import urlencode


class DbSpider(scrapy.Spider):
    name = 'db'
    allowed_domains = ['douban.com']
    start_urls = ['http://douban.com/']
    cookie_dict = {}
    header = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'

    def parse(self, response):

        cookie_jar = CookieJar()
        cookie_jar.extract_cookies(response, response.request)
        for k, v in cookie_jar._cookies.items():
            for i, j in v.items():
                for m, n in j.items():
                    self.cookie_dict[m] = n.value

        yield Request(url='https://accounts.douban.com/j/mobile/login/basic',
                      method='POST',
                      headers=self.header,
                      body=urlencode({'name':'13426798716',
                                      'password':'*****',
                                      'remember':'false',
                                      'ck':'',
                                      'ticket':''
                                      }),
                      cookies=self.cookie_dict,
                      callback=self.check_login)

    def check_login(self, response):
        print(response.text)
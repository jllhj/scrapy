# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.cookies import CookieJar
from scrapy.http import Request
from urllib.parse import urlencode


class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['github.com']
    start_urls = ['http://github.com/login']
    cookie_dict = {}

    def parse(self, response):
        r1 = response.xpath('//input[@name="authenticity_token"]/@value').extract_first()
        cookie_jar = CookieJar()
        cookie_jar.extract_cookies(response,response.request)
        for k, v in cookie_jar._cookies.items():
            for i, j in v.items():
                for m, n in j.items():
                    self.cookie_dict[m] = n.value
        yield Request(url='https://github.com/session',
                      method='POST',
                      body=urlencode({'commit':'Sign in',
                                      'utf8':'✓',
                                      'authenticity_token':r1,
                                      'login':'jllhj',
                                      'password':'*****',
                                      'webauthn-support':'supported'
                                      }),
                      cookies=self.cookie_dict,
                      callback=self.check_login)

    def check_login(self,response):
        yield Request(
            url='https://github.com/settings/emails',
            cookies=self.cookie_dict,
            callback=self.get_email
        )

    def get_email(self,response):
        # e1 = response.xpath('//span[@class="css-truncate-target"]/@title').extract_first()
        e1 = response.xpath('//span[@class="css-truncate-target"]/text()').extract_first()
        print(e1)
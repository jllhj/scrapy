# import scrapy
# from scrapy.http import Request,FormRequest
# import urllib.request
#
#
# class DbSpider(scrapy.Spider):
#     name = 'db'
#     allowed_domains = ['douban.com']
#     # start_urls = ['http://douban.com/']
#     header={"User-Agent:":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
#
#     def start_requests(self):
#         return [Request("https://accounts.douban.com/login",callback=self.parse,headers=self.header,meta={"cookiejar":1})]
#
#     def parse(self, response):
#         captcha=response.xpath("//img[@id='captcha_image']/@src").extract()
#         url="https://accounts.douban.com/login"
#
#         if len(captcha)>0:
#             print("此时有验证码")
#             localpath="D:/pythonlianxi/douban/captcha.png"
#             urllib.request.urlretrieve(captcha[0],filename=localpath) # 将验证码图片下载到本地再查看。
#             print("请查看本地验证码图片并输入验证码")
#             captcha_value=input()
#             data = {
#                 "form_email": "xxxxxxxx",
#                 "form_password": "xxxxxxx",
#                 "captcha_solution":captcha_value,
#                 "redir":"https://www.douban.com/people/xxxxxx/",
#             }
#         else:
#             print("此时没有验证码")
#             data={
#                 "form_email":"xxxxxxx",
#                 "form_password":"xxxxxxxx",
#                 "redir":"https://www.douban.com/people/xxxxxx/",
#             }
#         print("登录中")
#         return[FormRequest.from_response(response,
#                                          meta={"cookiejar":response.meta["cookiejar"]},#这是固定的用法。
#                                          headers=self.header,
#                                          formdata=data,
#                                          callback=self.next,
#                                          )]
#
#     def next(self,response):
#         print("此时已经登陆完成并爬取个人中心")
#         title=response.xpath("/html/head/title").extract()
#         print(title[0])

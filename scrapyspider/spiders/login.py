# -*- coding: utf-8 -*-
import scrapy, urllib
from scrapy.http import Request,FormRequest
from scrapyspider.items import MovieCommentItem

class LoginSpider(scrapy.Spider):

    name = "login"

    allowed_domains = ["douban.com"]

    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"}

    def start_requests(self):

        return [FormRequest("https://accounts.douban.com/login",headers=self.header,meta={"cookiejar":1},callback=self.parse)]


    def parse(self, response):

        captcha = response.xpath("//img[@id='captcha_image']/@src").extract()


        if len(captcha) > 0:

            print("此时有验证码.")

            localpath = "captcha.png"

            urllib.urlretrieve(captcha[0],filename = localpath)

            captchar_value = input("请到~/scrapy/scrapyspider/的captcha.png查看验证码:")

            data = {
                "captcha-solution":captchar_value,
                "redir": "https://www.douban.com/people/undergroundsky/",
                "form_email": "your_email",  #用户名
                "form_password": "your_code",  #用户密码
                "login": "登录",
            }


        else:

            data = {
                "redir": "https://www.douban.com/people/undergroundsky/",
                "form_email": "your_email",
                "form_password": "your_code",
                "login": "登录",
            }

        print("登陆中...")

        return [FormRequest.from_response(response,
                                          meta = {"cookiejar":response.meta["cookiejar"]},
                                          headers = self.header,
                                          # 设置POST表单中的数据
                                          formdata = data,
                                          # 设置回调函数，此时回调函数为next()
                                          callback = self.next,
                                          )]


    def next(self, response):

        title = response.xpath("/html/head/title/text()").extract()[0]

        print(title.encode('UTF-8'))


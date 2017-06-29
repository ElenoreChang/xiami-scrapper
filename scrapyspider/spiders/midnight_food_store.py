import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from scrapyspider.items import MovieCommentItem
from scrapy.conf import settings

class MFSCommentSpider(Spider):

    name = "midnight_food_store" 

    allowed_domains = ["douban.com"]

    start_urls = ["https://movie.douban.com/subject/26411410/comments"]
    
	
    cookie = settings['COOKIE']

    headers = {
        'Connection': 'keep - alive',  # 保持链接状态
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"
    }

    # 对请求的返回进行处理的配置
    meta = {
        'dont_redirect': True,  # 禁止网页重定向
        'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
    }

    def start_requests(self):
        # 带着cookie向网站服务器发请求，表明我们是一个已登录的用户
        yield Request(self.start_urls[0], callback=self.parse, cookies=self.cookie,
                      headers=self.headers, meta=self.meta)

 
    def parse(self, response):

        item = MovieCommentItem()

        comments = response.xpath('//div[@class="mod-bd"]/div[@class="comment-item"]')

        for content in comments:

            item['user_name'] = content.xpath(
				'.//span[@class="comment-info"]/a/text()').extract()

            item['user_id'] = content.xpath(
				'.//span[@class="comment-info"]/a/@href').re(r'https://www.douban.com/people/*(.*)/')

            item['comment_time'] = content.xpath(
				'.//span[@class="comment-time "]/text()').extract()

            item['comment'] = content.xpath(
				'.//p/text()').extract()

            item['usefule_num'] = content.xpath(
				'.//span[@class="votes"]/text()').extract()

            item['ranking'] = content.xpath(
				'.//span[contains(@class,"allstar")]/@title').extract()

            yield item

        next_url = response.xpath('//a[@class="next"]/@href').extract()

        if next_url:

            next_url = 'https://movie.douban.com/subject/26411410/comments' + next_url[0]

            yield Request(next_url, headers=self.headers)

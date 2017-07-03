scrapy爬虫——爬取豆瓣影评
====

最近用scrapy写了一个爬取豆瓣影评的爬虫。在这里把步骤以及解决相关问题的思路写一下。首先介绍一下我使用的工具和环境。
> **工具和环境**
> 1. 系统：ubuntu 16.4
> 2. 语言： python 2.7
> 3. IDE： sublime text 3
> 4. 浏览器： Chrome
> 5. 爬虫框架：Scrapy 1.0.3 

这篇文章主要介绍如何在 linux 系统下安装 scarpy， 如何编写一个简单的爬虫，以及如何处理登录豆瓣的问题。如果你有兴趣了解本文的爬虫代码，可以[戳这里](https://github.com/ElenoreChang/douban_movie_comment_spider).
<!--more-->


## 安装 Scrapy
按照[最新的官方文档](http://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/ubuntu.html)中的教程进行安装，注意不要使用 Ubuntu 提供的 `python-scrapy`，因为相较于最新版的 Scrapy，该包版本太旧，并且运行速度也较为缓慢。上述教程中使用的是 [Scrapinghub](http://scrapinghub.com/) 发布的 apt-get 可获取版本。
关于 Scrapy 的架构及各组建作用在官方文档中也有介绍。
## 新建 Scrapy 爬虫项目 
在terminal中进入你为爬虫项目建立的目录中，运行以下命令：
```shell
scrapy startproject scrapyspider
``` 
这个命令会在该目录中创建以下结构的 scrapyspider 目录：
```
scrapyspider/
    scrapy.cfg
    scrapyspider/
        __init__.py
        items.py
        pipelines.py
        settings.py
        spiders/
            __init__.py
            ...
```
这些文件分别是:
- `scrapy.cfg`: 项目配置文件。
- `tutorial/`: 该项目的 python 模块。之后您将在此加入代码。
- `tutorial/items.py`: 项目中的 item 文件。
- `tutorial/pipelines.py`: 项目中的 pipelines 文件。
- `tutorial/settings.py`: 项目的设置文件。
- `tutorial/spiders/`: 放置 spider 代码的目录。

### 声明 Item 类
在编写爬虫代码之前，需要先确定需要爬取的数据的结构，即需要哪些字段，观察待爬取的网页，看看哪些信息是需要保存下来的有用字段。

![](http://i650.photobucket.com/albums/uu224/dearelenore/Screenshot%20from%202017-06-30%2010-49-24_zpscgcfmihb.png)

在这里，我希望获取的影评数据的字段包括：
> - `user_name`：撰写影评的用户名
> - `user_id`：用户ID
> - `comment_time`：评论时间
> - `ranking`：评分
> - `comment`：短评内容
> - `useful_num`：被其他用户标记为“有用”的次数 


因此为了获得上述的结构性数据，我们需要在 `items.py` 中编写声明 Item 的代码：

``` python
class MovieCommentItem(scrapy.Item):

	user_name = scrapy.Field()

	user_id = scrapy.Field()

	comment_time = scrapy.Field()

	ranking = scrapy.Field()

	comment = scrapy.Field()

	usefule_num = scrapy.Field()
```

### 编写爬虫代码 
在 `scrapyspider/spiders` 目录下新建一个爬虫文件，因为我将要爬取的是电影深夜食堂（中国版）的影评，我将其命名为 `midnight_food_store.py`. 
在编写爬虫代码之前，需要先确定我们需要获取的信息位于待爬取网页的什么位置，如何定位它。在 Chrome 中打开待爬取页面，按 F12 打开开发者工具，检查网页的源代码，发现我们需要获取的每个短评都位于一个 class 为 comment-item 的 div 标签中。具体的爬虫代码如下：

``` python
from scrapy import Request
from scrapy.spiders import Spider
from scrapyspider.items import MovieCommentItem

class MFSCommentSpider(Spider):

    name = "midnight_food_store"
   
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }
    

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

```

### 解决问题
上述代码基本实现了从豆瓣爬取影评的功能，且能够自动翻页。但是由于豆瓣有反爬虫的机制，对于没有登录的用户只能爬取十页内容。因此还需要爬虫在启动时能够登录豆瓣。为了解决这个问题，我依次尝试了三种方法，最后使用cookie保持登录状态的方法成功登录并爬取了影评数据。
#### 方法1 ： 简单登录
按照官方推荐的方法，为了在启动爬虫时自动以 POST 登录豆瓣，需要重写 `start_request()` 方法，如下：
```python
def start_requests(self):
        return [scrapy.Request("https://accounts.douban.com/login",meta={'cookiejar':1},callback=self.post_login)]

def post_login(self,response):
        print 'Let's go ...'

        return [scrapy.FormRequest.from_response(response,
            meta={'cookiejar':response.meta['cookiejar']},
            headers = self.headers,
            formdata={
            'form_email':'your_email',
            'form_password':'your_code'
            },callback=self.checkLogin,
            dont_filter=True)]

```
起初使用该方法是可行的，但连续登录几次之后再次登录需要输入验证码，因此该方法失效。 

#### 方法2：半自动输入验证码 

通过查找谷歌发现一种手动输入验证码的方式，思路是在上一种方法的基础上，当多次登录出现验证码之后，将验证码图片保存到本地，然后手动查看并输入验证码。代码如下 ：
```python
import scrapy
from scrapy.http import Request,FormRequest
import urllib
from scrapyspider.items import MovieCommentItem

class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['douban.com']
    #start_urls = ['http://douban.com/']
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"}

    def start_requests(self):
        return [FormRequest("https://accounts.douban.com/login",headers=self.header,meta={"cookiejar":1},callback=self.parse)]

    def parse(self, response):
        captcha = response.xpath("//img[@id='captcha_image']/@src").extract()
        if len(captcha) > 0:
            print("此时有验证码.")
            localpath = "captcha.png"
            urllib.urlretrieve(captcha[0],filename=localpath)
            captchar_value = input("请到~/scrapy/scrapyspider/的captcha.png查看验证码是什么？")
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
                "form_password": "your_code,
                "login": "登录",
            }
        print("登陆中...")
        return [FormRequest.from_response(response,
                                          meta={"cookiejar":response.meta["cookiejar"]},
                                          headers=self.header,
                                          # 设置POST表单中的数据
                                          formdata=data,
                                          # 设置回调函数，此时回调函数为next()
                                          callback=self.next,
                                          )]

    def next(self, response):
        title = response.xpath("/html/head/title/text()").extract()[0]
        print(title.encode('UTF-8'))

```
这个方法在出现验证码的时候可以成功登录，但是当使用该方法登录并爬取数据时会报错，而且google了很久也没有找到相应的解决办法，只能放弃该方法。

#### 方法3：带 cookie 发出 Request 请求
方法3采用的是[这篇文章](http://kongtianyi.cn/2016/10/15/python/Scrapy-Lesson-5/?utm_source=tuicool&utm_medium=referral)中提出的通过配置 cookie 保持登录状态的方法，文章中也给出了该方法的原理：
>  一般情况下，网站通过存放在客户端的一个被称作cookie的小文件来存放用户的登陆信息。在浏览器访问网站的时候，会把这个小文件发往服务器，然后服务器根据这个小文件确定你的身份，然后返回给你特定的信息。

> 我们要做的就是尽量模拟浏览器的行为，在使用爬虫访问网站时也带上cookie来访问。

该方法包括以下几个步骤：
1. 获取 cookie
2. 转换 cookie 的格式
3. 在 `settings.py` 中给 scrapy 配置 cookie
4. 编写爬虫文件

按照原作者的第一步的方法从浏览器获取到的 cookie 是字符串格式的，而在 scrapy  中，配置 cookie 需要是字典格式的，因此该作者编写了一个脚本来进行转换：
```python
# -*- coding: utf-8 -*-

class transCookie:
    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        '''
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        '''
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict

if __name__ == "__main__":
    cookie = "你复制出的cookie"
    trans = transCookie(cookie)
    print trans.stringToDict()

```

将上述脚本 print 出的字典格式的 cookie 复制到 `settings.py` 中，然后在爬虫文件中使爬虫发起带有 cookie 的 Request  请求， 就可以省去处理登录以及验证码的过程了。具体的教程可以点进原文查看。这个方法最终证实是有效的。

#### 总结
使用上面方法编写的爬虫程序，我爬取了豆瓣上面关于国产版《深夜食堂》的 47650 条短评。使用这些数据，可以做一些基础的数据分析。



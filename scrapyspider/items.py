# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MovieCommentItem(scrapy.Item):

	user_name = scrapy.Field()

	user_id = scrapy.Field()

	comment_time = scrapy.Field()

	ranking = scrapy.Field()

	comment = scrapy.Field()

	usefule_num = scrapy.Field()

	

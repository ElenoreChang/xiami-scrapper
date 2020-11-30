# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AlbumSongItem(scrapy.Item):
    #album_id = scrapy.Field()
    album_name = scrapy.Field()
    #artist_id = scrapy.Field()
    artists = scrapy.Field()
    info = scrapy.Field()
    tags = scrapy.Field()
    album_publish_date = scrapy.Field()
    disc_id = scrapy.Field()
    song_index = scrapy.Field()
    song_name = scrapy.Field()
    song_singer = scrapy.Field()
    song_dur = scrapy.Field()
    play_cnt = scrapy.Field()

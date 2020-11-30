虾米个人收藏音乐人专辑爬虫
====
爬取指定虾米用户收藏的音乐人所有专辑歌曲详情，包含字段：
```python
import scrapy
class AlbumSongItem(scrapy.Item):
    album_name = scrapy.Field() #专辑名称
    artists = scrapy.Field() #音乐人（列表）
    info = scrapy.Field() #专辑信息（包含厂牌、语言、类别等）
    tags = scrapy.Field() #专辑标签（列表）
    album_publish_date = scrapy.Field() #专辑发行日期
    disc_id = scrapy.Field() #disc id
    song_index = scrapy.Field() #歌曲在disc中所在位置
    song_name = scrapy.Field() #歌曲名称
    song_singer = scrapy.Field() #歌手（列表）
    song_dur = scrapy.Field() #歌曲时长
    play_cnt = scrapy.Field() #播放量
```
执行 `scrapy crawl user_fav_page_scrapper -o data.csv -a user_id=xxx begin_page=1 end_page=1` 会将结果保存在当前目录下的 data.csv 文件中





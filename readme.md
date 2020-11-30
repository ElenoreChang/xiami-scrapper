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
修改 `./run.sh` 中的 user_id begin_page（开始页） 和 end_page （结束页）后，在终端 ./run.sh 执行，结果将保存于 `data_${begin_page}_${end_page}.csv` 文件中

结果示例：
```
album_name	album_publish_date	artists	disc_id	info	play_cnt	song_dur	song_index	song_name	song_singer	tags
Wild Heart	2013-01-02	Current Joys	Disc 1	{'专辑语种': '英语', '厂牌': 'Self-Released', '专辑类别': '录音室专辑'}	864	02:35	1	My Blood	Current Joys	卧室流行
Wild Heart	2013-01-02	Current Joys	Disc 1	{'专辑语种': '英语', '厂牌': 'Self-Released', '专辑类别': '录音室专辑'}	3349	03:46	2	New York City	Current Joys	卧室流行
Wild Heart	2013-01-02	Current Joys	Disc 1	{'专辑语种': '英语', '厂牌': 'Self-Released', '专辑类别': '录音室专辑'}	566	02:37	3	Televisions	Current Joys	卧室流行
Wild Heart	2013-01-02	Current Joys	Disc 1	{'专辑语种': '英语', '厂牌': 'Self-Released', '专辑类别': '录音室专辑'}	429	03:14	4	Blade Running	Current Joys	卧室流行
Wild Heart	2013-01-02	Current Joys	Disc 1	{'专辑语种': '英语', '厂牌': 'Self-Released', '专辑类别': '录音室专辑'}	1295	02:48	5	New Flesh	Current Joys	卧室流行
Wild Heart	2013-01-02	Current Joys	Disc 1	{'专辑语种': '英语', '厂牌': 'Self-Released', '专辑类别': '录音室专辑'}	1.0万	03:15	6	Blondie	Current Joys	卧室流行
Wild Heart	2013-01-02	Current Joys	Disc 1	{'专辑语种': '英语', '厂牌': 'Self-Released', '专辑类别': '录音室专辑'}	383	02:32	7	I'm Terrified	Current Joys	卧室流行
Wild Heart	2013-01-02	Current Joys	Disc 1	{'专辑语种': '英语', '厂牌': 'Self-Released', '专辑类别': '录音室专辑'}	4230	03:02	8	Symphonia IX (Grimes Cover)	Current Joys	卧室流行
Wild Heart	2013-01-02	Current Joys	Disc 1	{'专辑语种': '英语', '厂牌': 'Self-Released', '专辑类别': '录音室专辑'}	388	03:14	9	Strange Life	Current Joys	卧室流行
Wild Heart	2013-01-02	Current Joys	Disc 1	{'专辑语种': '英语', '厂牌': 'Self-Released', '专辑类别': '录音室专辑'}	1023	07:09	10	You Broke My Heart	Current Joys	卧室流行
The Captain	2009-09-09	Biffy Clyro	Disc 1	{'专辑语种': '英语', '厂牌': '14th Floor Records', '专辑类别': '录音室专辑'}	544	03:22	1	The Captain	Biffy Clyro	流行
```
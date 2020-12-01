虾米个人收藏音乐人专辑爬虫
====
## 需求来源
需求来自豆瓣友邻广播
https://www.douban.com/people/binchoutan/status/3194376103/


## 功能描述
爬取指定虾米用户收藏的音乐人所有专辑歌曲详情，包含字段：

| 字段名 | 字段描述 | 字段类型 |
| --- | --- | --- |
| album_name | 专辑名称 | 字符串 |
| artists | 音乐人 | 列表 |
| info | 专辑信息（包含厂牌、语言、类别等） | json 字符串 |
| tags | 专辑标签 | 列表 | 
| album_publish_date | 专辑发行日期  | 字符串 |
| disc_id | disc id | 字符串 |
| song_index | 歌曲在 disc 中所在位置 | 整数型 |
| song_name | 歌曲名称 | 字符串 |
| song_singer | 歌手 | 列表 |
| song_dur | 歌曲时长 | 字符串，mm:ss |
| play_cnt | 播放量 | 整数型 |

## 如何使用
### Python 环境安装
此项目运行于 Python 3.6 环境下，需要先安装对应版本的 Python 环境，[下载地址](https://www.python.org/ftp/python/3.6.10/Python-3.6.10.tgz)
环境部署可以参考[廖雪峰的教程](https://www.liaoxuefeng.com/wiki/1016959663602400/1016959856222624)

### 依赖安装
安装好 Python 之后，打开命令行，执行 `pip3 install scrapy` 安装爬虫依赖的 `scrapy` 工具包
如果安装速度很慢或者报错的话，可以执行`pip install --index-url https://pypi.douban.com/simple scipy`命令，将源切换到豆瓣

### 执行程序
1. 将本项目下载或 clone 到本地
2. 将自己的cookie复制粘贴到 `./cookie.txt` 中 (ref: [如何查看自己的cookie](https://blog.csdn.net/MuWinter/article/details/75313476))
3. 修改项目代码中的 `run.sh` 脚本，修改 user_id begin_page 和 end_page 的赋值，然后在命令行运行该脚本，如代码保存在了 `~/Desktop/` 下，则在命令行输入 `cd ~/Desktop/xiami-scrapper; ./run.sh`
脚本将提交三个并行的爬虫进程在后台运行，为了防止 xiami 启动反爬虫机制，设置了 3s 的 DOWNLOAD_DELAY，如果觉得运行比较慢的话也可以自己手动修改 `settings.py` 中 DOWNLOAD_DELAY 的值。
4. 要终止程序，在命令行执行 `./kill_crawl.sh` ，则会将爬虫进程杀死
5. 数据会保存在 `./data/` 路径下

### 执行速度
目前执行速度
INFO: Crawled 28 pages (at 3 pages/min), scraped 70 items (at 40 items/min)

## 结果示例：
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

## 解决问题列表
- 网页重定向问题
- 多进程控制
- 带 cookie 请求

from scrapy import Request
from scrapy.spiders import Spider
from scrapyspider.items import AlbumSongItem
from scrapyspider.trans_cookie import TransCookie


class UserFavArtistAlbumScrapper(Spider):
    name = "user_fav_page_scrapper"

    allowed_domains = ["xiami.com"]

    cookie = None
    user_id = 11111
    cur_page = 1
    headers = {
        'Connection': 'keep - alive',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"
    }

    # 对请求的返回进行处理的配置
    meta = {
        'dont_redirect': True,  # 禁止网页重定向
        'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
    }

    def start_requests(self):
        user_id = getattr(self, 'user_id', 11111)
        self.user_id = user_id
        begin_page = getattr(self, 'begin_page', 1)
        self.cur_page = int(begin_page)

        transCookie = TransCookie()
        self.cookie = transCookie.stringToDict()
        self.logger.info(f"crawling website using cookie {self.cookie}")
        start_url = f"https://www.xiami.com/list?page={begin_page}&query=%7B%22userId%22%3A%22{user_id}%22%7D&scene=favorite&type=artist"

        yield Request(start_url, callback=self.parse, cookies=self.cookie,
                      headers=self.headers, meta=self.meta)

    def parse(self, response):
        """
        解析用户收藏音乐人列表页，逐个进入音乐人专辑列表页
        :param response:
        :return:
        """
        # cur_page_id = self.get_page_id_from_url(response.request.url)
        self.logger.info(f"parsing user fav artists list page of page {self.cur_page}")
        end_page = int(getattr(self, 'end_page', 10))
        artists_list_content = response.xpath('//div[@class="adaptive-list"]/div[@class="artist-item unselectable"]')
        for artist_card in artists_list_content:
            artist_id = artist_card.xpath('./a/@href').re('artist/(.*)')[0]
            artist_name = artist_card.xpath('./div[@class="info"]/div[@class="name"]/a/text()').extract()[0]
            artist_albums_page_url = f"https://www.xiami.com/list?scene=artist&type=album&query=%7B%22artistId%22:%22{artist_id}%22%7D"
            yield Request(url=artist_albums_page_url, headers=self.headers, cookies=self.cookie,
                        callback=self.parse_artist_albums_page, meta={'artist_name': artist_name})

        if len(artists_list_content) > 0 and self.cur_page < end_page:
            self.cur_page += 1
            next_url = f"https://www.xiami.com/list?page={self.cur_page}&query=%7B%22userId%22%3A%22{self.user_id}%22%7D&scene=favorite&type=artist"

            yield Request(url=next_url, headers=self.headers, cookies=self.cookie,
                          callback=self.parse)


    # def parse_artist_page(self, response):
    #     """
    #     解析音乐人详情页，获取音乐人专辑列表页
    #     :param response:
    #     :return:
    #     """
    #
    #     artist_name = response.xpath(
    #         '//div[@class="artist-info"]/div[@class="titleInfo"]/div[@class="titleInfo-name"]/text()').extract()[0]
    #     self.logger.info(f"parsing artist detail page of {artist_name}")
    #     artist_albums_page_req = \
    #         response.xpath('//div[@class="related-albums"]/div[@class="blocktitle"]/a/@href').extract()[0]
    #     artist_id = response.xpath('//div[@class="related-albums"]/div[@class="blocktitle"]/a/@href').re('artist/(.*)?spm=')
    #     artist_albums_page_url = f"https://www.xiami.com/list?scene=artist&type=album&query=%7B%22artistId%22:%22{artist_id}%22%7D"
    #     yield Request(url=artist_albums_page_url, headers=self.headers, cookies=self.cookie,
    #                   callback=self.parse_artist_albums_page)


    def parse_artist_albums_page(self, response):
        """
        解析音乐人专辑列表页，逐个进入专辑详情页，此列表页不分页？
        :param response:
        :return:
        """
        artist_name = response.meta['artist_name']
        self.logger.info(f"parsing {artist_name}'s album list page")
        album_list_content = response.xpath('//div[@class="adaptive-list"]/div[@class="album-item unselectable"]')

        if len(album_list_content) == 0:
            self.logger.info("artist album list empty")
            return

        for album_card_content in album_list_content:
            album_page_req = album_card_content.xpath('./div[@class="wrapper"]/a/@href').extract()[0]
            album_name = album_card_content.xpath('./div[@class="info"]/div[@class="name"]/a/text()').extract()[0]
            album_page_url = f'https://xiami.com{album_page_req}'
            yield Request(url=album_page_url, headers=self.headers, cookies=self.cookie,
                          callback=self.parse_album_page, meta={'album_name':album_name})


    def parse_album_page(self, response):
        """
        解析专辑详情页
        :param response:
        :return:
        """
        album_name = response.meta['album_name']
        album = []
        album_info = response.xpath('//div[@class="album-info"]/div[@class="titleInfo"]')
        #album_name = album_info.xpath('.//div[@class="titleInfo-name"]/text()').extract()[0]
        self.logger.info(f"parsing album detail page of {album_name}")
        artists_info = album_info.xpath('.//div[@class="singer-item"]')
        artists = []
        for artist_info in artists_info:
            artist_name = artist_info.xpath('.//div[@class="singer-name"]/text()').extract()[0]
            artists.append(artist_name)
        album_publish_date = album_info.xpath('.//div[contains(@style, "color:gray")]/text()').extract()[0]

        tags = []
        tags_content = album_info.xpath('.//div[@class="tags"]')
        for tag_content in tags_content:
            tag = tag_content.xpath('.//span[@class="tag-item"]/a/text()').extract()[1]
            tags.append(tag)

        infos_content = response.xpath(
            '//div[@class="leftbar-inner"]/div[@class="leftbar-content"]/div[@class="infos"]/div[@class="info-panel"]/div[@class="info"]')
        info = {}
        for info_content in infos_content:
            info_name = info_content.xpath('.//div[@class="info-name"]/text()').extract()[0]
            if info_name in ['厂牌', '专辑语种', '专辑类别']:
                try:
                    if info_name == '厂牌':
                        info_value = info_content.xpath('.//div[@class="info-value"]/div/a/div/text()').extract()[0]
                    else:
                        info_value = info_content.xpath('.//div[@class="info-value"]/text()').extract()[0]
                except:
                    info_value = ''
                info[info_name] = info_value

        discs_info = response.xpath('.//div[@class="disc"]')
        for disc_info in discs_info:
            disc_id = disc_info.xpath('.//h3/text()').extract()[0]
            songs_info = disc_info.xpath('.//div[@class="table idle song-table"]/div/table/tbody/tr')
            index = 1
            for song_info in songs_info:
                tr_class = song_info.xpath('@class').extract()[0]
                if tr_class != 'extended-row odd' and tr_class != 'extended-row even':
                    album_song = AlbumSongItem()

                    album_song['song_index'] = index
                    song_name_container = song_info.xpath('.//div[@class="songName-container"]')
                    album_song['song_name'] = song_name_container.xpath('.//a/text()').extract()[0]
                    singers_container = song_info.xpath('.//div[@class="artist-container"]/div/a')
                    singer_names = []
                    for singer_info in singers_container:
                        singer_name = singer_info.xpath('./text()').extract()[0]
                        singer_names.append(singer_name)
                    album_song['song_singer'] = singer_names
                    try:
                        album_song['play_cnt'] = \
                            song_info.xpath('.//div[@class="playCount-container"]/text()').extract()[0]
                        album_song['song_dur'] = song_info.xpath('.//span[@class="duration"]/text()').extract()[0]
                    except:
                        album_song['play_cnt'] = 0
                        album_song['song_dur'] = ''

                    album_song['artists'] = artists
                    album_song['album_name'] = album_name
                    album_song['album_publish_date'] = album_publish_date
                    album_song['tags'] = tags
                    album_song['info'] = info
                    album_song['disc_id'] = disc_id

                    album.append(album_song)
                    index += 1

        return album

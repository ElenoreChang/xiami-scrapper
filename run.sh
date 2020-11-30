begin_page=1
end_page=1
user_id=860643
scrapy crawl user_fav_page_scrapper \
  	 -o data_${begin_page}_${end_page}.csv \
	 -a user_id=${user_id} \
	 -a begin_page=${begin_page} \
	 -a end_page=${end_page}

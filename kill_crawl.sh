kill -9 $(ps -ef | grep crawl| grep -v grep | awk '{print $2}')

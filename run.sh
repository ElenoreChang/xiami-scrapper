
#!/bin/bash
dir=$(pwd) #当前路径
begin_page=1 #爬取开始页
end_page=1 #爬取结束页
user_id=860643 #用户id

thread=3 #最大进程数

mkdir $dir/data/
mkdir $dir/log/
# Step1 创建有名管道
[ -e ./fd1 ] || mkfifo ./fd1

# 创建文件描述符，以可读（<）可写（>）的方式关联管道文件，这时候文件描述符3就有了有名管道文件的所有特性
exec 3<> ./fd1

# 关联后的文件描述符拥有管道文件的所有特性,所以这时候管道文件可以删除，我们留下文件描述符来用就可以了
rm -rf ./fd1

# Step2 创建令牌
for i in `seq 1 $thread`;
do
    # echo 每次输出一个换行符,也就是一个令牌
    echo >&3
done

# Step3 拿出令牌，进行并发操作
for page in `seq $begin_page $end_page`;
do
    read -u3                    # read 命令每次读取一行，也就是拿到一个令牌
    {
        echo "crawling user fav artist page $page"
        scrapy crawl user_fav_page_scrapper \
  	      -o $dir/data/data_${page}.csv \
	        -a user_id=${user_id} \
	        -a begin_page=${page} \
	        -a end_page=${page} \
	        --logfile $dir/log/log_$page.txt
        echo >&3                # 执行完一条命令会将令牌放回管道
    }&
done

wait

exec 3<&-                       # 关闭文件描述符的读
exec 3>&-                       # 关闭文件描述符的写


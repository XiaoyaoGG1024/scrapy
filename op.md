创建项目
scrapy  startproject scrapyDemo01
创建目标程序 
scrapy genspider 文件名  url
scrapy genspider  movie  movie.douban.com
运行
scrapy crawl movie --nolog
scrapy crawl name -o 文件名
scrapy crawl movie -o douban.csv

pip freeze > requirements
pip install -r requirements

保存设置 settings
ITEM_PIPELINES
中间件settings
DOWNLOADER_MIDDLEWARES

https://www.nba.com/players
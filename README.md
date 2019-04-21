# weixinspider
通过关键字爬取微信公众好号相关文章

关键字存在文件/res/keywords.txt里面
启动程序为/spiders/setup.py
使用了scrapy框架，借用了壳
使用selenium库，驱动chrome浏览器
程序的数据存在远程数据库，数据库使用的是postgresql，配置文件为config.py，数据库连接程序在piplines.py


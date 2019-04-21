# weixinspider
通过关键字爬取微信公众号相关文章

关键字存在文件/res/keywords.txt里面

启动程序为/spiders/setup.py

使用了scrapy框架，借用了壳

使用selenium库，驱动chrome浏览器

程序的数据存在远程数据库，数据库使用的是postgresql，配置文件为config.py，数据库连接程序在piplines.py

通过微信搜狗查询微信公众号文章，查询过程中ip会被封，会弹出人机验证页面，程序没有处理而是选择结束，存入已经爬取的数据。查询过程中考虑到人工和登录方式的问题，始终没有登录微信。所以最多只能爬取到100篇文章。

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2
import hashlib
from .config import *

class WeixinSpiderPipeline(object):
    def __init__(self):
        try:
            self.conn = psycopg2.connect(database=POSTGRES_DBNAME, user=POSTGRES_USER, password=POSTGRES_PASSWD,
                                         host=POSTGRES_HOST, port=POSTGRES_PORT)
            print("Connect successfully")
        except Exception as e:
            print(e)
            self.conn.rollback()

    def process_item(self, item, spider):
        content = item['content'].encode('utf-8')
        searchstr = item['searchstr'].encode('utf-8')
        url = item['url'].encode('utf-8')
        title = item['title'].encode('utf-8')
        md5 = hashlib.md5()  # 应用MD5算法
        md5.update(title)
        titleMD5 = md5.hexdigest()
        username = item['username'].encode('utf-8')
        md5.update(username)
        usernameMD5 = md5.hexdigest()
        uniid = (str(titleMD5) + str(usernameMD5)).encode('utf-8')
        source = "weixin".encode('utf-8')
        device = "weixin".encode('utf-8')
        sendtime = item['sendtime'].encode('utf-8')
        scraptime = item['scraptime'].encode('utf-8')
        SELCT_IF_EXIST = "SELECT title FROM scrapiesrestb WHERE uniid = '%s';"
        cursor = self.conn.cursor()
        cursor.execute(SELCT_IF_EXIST % (uniid.decode()))
        rows = cursor.fetchall()
        if len(rows) > 0:
            print("重复")
        else:
            sql = "insert into scrapiesrestb(content, scraptime, source, url, username, uniid, searchstr, device, sendtime,title) values('%s','%s', '%s', '%s', '%s','%s','%s','%s','%s','%s');"
            print("执行：insert")
            cursor.execute(sql % (
            content.decode(), scraptime.decode(), source.decode(), url.decode(), username.decode(), uniid.decode(),
            searchstr.decode(), device.decode(), sendtime.decode(), title.decode()))
            self.conn.commit()
        return item

    def close_spider(self, spider):
        self.conn.close()

    def open_spider(self, spider):
        pass

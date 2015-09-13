#! /usr/bin/python

import __init__

import newspaper
from queue import redis_queue
from database import mysql
import hashlib
import json
import time

class MysqlWriter(object):
    """Crawler class prepares a news source and writes it into the redis queue"""
    def __init__(self):
        self.queue = redis_queue.connect()
        self.p = self.queue.pubsub()
        self.p.subscribe('newssource-channel')
        self.conn=mysql.connect()
        self.cursor = self.conn.cursor()

    def run(self):
        for message in self.p.listen():
            self.message = message
            self.write_to_mysql()

    def write_to_mysql(self):
        self.write_article()
        self.write_category()

    def write_article(self):
        base_sql = "INSERT INTO article (id,url,newssource,crawled_at) VALUES "
        end_sql = " ON DUPLICATE KEY UPDATE url=url"
        sql = base_sql
        to_insert = ""
        if(self.message['data']==1L):
            return
        data = json.loads(self.message['data'])
        articles = data['articles']
        cleaned_newssource = str(data['newssource'].replace("\"","\\\"").replace("\'","\\\'").strip())
        count = 0
        for article in articles:
            cleaned_article = str(article.replace("\"","\\\"").replace("\'","\\\'").strip())
            key = str(hashlib.sha1(cleaned_article).hexdigest())
            crawled_at = str(int(time.time()))
            to_insert="(\""+key+"\",\""+cleaned_article+"\",\""+cleaned_newssource+"\","+crawled_at+"),"
            sql+=to_insert
            count+=1
            if(count%100==0):
                sql=sql[:-1]+end_sql
                mysql.write(sql, self.cursor, self.conn)
                sql = base_sql
        sql=sql[:-1]
        if(sql[-1] == ")"):
            sql=sql+end_sql
            mysql.write(sql, self.cursor, self.conn)

    def write_category(self):
        base_sql = "INSERT INTO category (id,url) VALUES "
        end_sql = " ON DUPLICATE KEY UPDATE url=url"
        sql = base_sql
        to_insert = ""
        if(self.message['data']==1L):
            return
        data = json.loads(self.message['data'])
        categories = data['categories']
        count = 0
        for category in categories:
            cleaned_category = str(category.replace("\"","\\\"").replace("\'","\\\'").strip())
            key = str(hashlib.sha1(cleaned_category).hexdigest())
            to_insert="(\""+key+"\",\""+cleaned_category+"\"),"
            sql+=to_insert
            count+=1
            if(count%100==0):
                sql=sql[:-1]+end_sql
                mysql.write(sql, self.cursor, self.conn)
                sql = base_sql
        sql=sql[:-1]
        if(sql[-1] == ")"):
            sql=sql+end_sql
            mysql.write(sql, self.cursor, self.conn)

if __name__ == "__main__":
    test = MysqlWriter()
    test.run()
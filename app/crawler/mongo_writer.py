#! /usr/bin/python

import __init__

import newspaper
# from newspaper import source
from queue import redis_queue
from database import mongo
import hashlib
import json
import time
from newspaper.article import Article

class MongoWriter(object):
    """Crawler class prepares a news source and writes it into the redis queue"""
    def __init__(self):
        self.queue = redis_queue.connect()
        self.p = self.queue.pubsub()
        self.p.subscribe('newssource-channel')
        self.db = mongo.connect()

    def run(self):
        for message in self.p.listen():
            self.message = message
            self.write_to_mongo()

    def write_to_mongo(self):
        self.write_article()
    #     self.write_category()

    def write_article(self):
        if(self.message['data']==1L):
            return
        collection = self.db['articles']
        data = json.loads(self.message['data'])
        articles = data['articles']
        payloads = []
        count = 0;
        for article_url in articles:
            article = Article(article_url)
            article.build()
            payload = {}
            payload['meta_keywords'] = article.meta_keywords
            payload['title'] = article.title
            payload['url'] = article.url
            payload['text'] = article.text
            payload['html'] = article.html
            payload['keywords'] = article.keywords
            payload['_id'] = str(hashlib.sha1(article.title).hexdigest())
            payload['crawled_at'] = str(int(time.time()))
            payloads.append(payload)
            count+=1
            if(count%100==0):
                collection.insert_many(payloads)
                payloads = []
        if payloads:
            collection.insert_many(payloads)    

if __name__ == "__main__":
    test = MongoWriter()
    test.run()
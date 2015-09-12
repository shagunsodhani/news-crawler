#! /usr/bin/python

import __init__

from os.path import dirname, join, abspath
import newspaper
from queue import redis_queue
import json

class Crawler(object):
    """Crawler class prepares a news source and writes it into the redis queue"""
    def __init__(self):
        self.queue = redis_queue.connect()

    def crawl_all(self):
        filepath = dirname(dirname(dirname(abspath(__file__))))+"/data/sources.txt"
        with(open(filepath)) as infile:
            for line in infile:
                self.crawl(line.strip())

    def crawl(self, news_source_url):
        news_source = newspaper.build(news_source_url, dry=False)
        jsonified_news_source = self.jsonify(news_source)
        self.queue.publish('newssource-channel', jsonified_news_source)

    def jsonify(self, news_source):
        data = {}
        data['articles'] = []
        data['published'] = []
        for article in news_source.articles:
            data['articles'].append(article.url)
            article.get_publish_timestamp()
            published_at = article.publish_timestamp
            data['published'].append(published_at)
        data['newssource'] = news_source.url
        return json.dumps(data)

if __name__ == "__main__":
    crawl = Crawler()
    crawl.crawl_all()
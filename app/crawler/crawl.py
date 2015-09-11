#! /usr/bin/python

import __init__

from os.path import dirname, join, abspath
import newspaper
from queue import redis_queue

class Crawler(object):
    """Crawler class prepares a news source and writes it into the redis queue"""
    def __init__(self):
        self.queue = redis_queue.connect()

    def crawl_all(self):
        filepath = dirname(dirname(dirname(abspath(__file__))))+"/data/sources.txt"
        with(open(filepath)) as infile:
            for line in infile:
                print line
                self.crawl(line.strip())

    def crawl(self, news_source_url):
        news_source = newspaper.build(news_source_url, dry=True)
        print news_source
        self.queue.publish('newssource-channel', news_source)

if __name__ == "__main__":
    crawl = Crawler()
    crawl.crawl_all()
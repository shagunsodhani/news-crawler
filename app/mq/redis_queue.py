#! /usr/bin/python

from os import path
from configparser import ConfigParser

import redis

#parse config
config=ConfigParser()
config.read(path.join(path.dirname(path.dirname(path.abspath(__file__))), 'config', 'config.cfg'))

def connect(service_name="redis"):
    host=config.get(service_name,"host")
    port=config.get(service_name,"port")
    db=config.get(service_name,"db")
    r = redis.StrictRedis(host=host, port=port, db=db)
    return r

if __name__ == "__main__":
    print(connect())
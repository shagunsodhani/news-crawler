#! /usr/bin/python

from os import path
from ConfigParser import ConfigParser

#parse config
config=ConfigParser()
config.read(path.join(path.dirname(path.dirname(path.abspath(__file__))), 'config', 'config.cfg'))

from pymongo import MongoClient

def connect(service_name="mongo"):
    host=config.get(service_name,"host")
    port=config.get(service_name,"port")
    db=config.get(service_name, "db")
    client = MongoClient(host, int(port))
    database = client[db]
    return database

if __name__ == "__main__":
	print connect()
#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import feedparser
import re
import urllib2
import xml.etree.ElementTree as ET
from utility_common import *
from index_gravitytales import get_index
import time


def parse_feed(feed_url):
  releases = []
  print '1'
  feed = feedparser.parse(feed_url)
  print '2'
  for entry in feed.entries:
    link = strip_unicode(entry.link)
    links = find_links(link, 'http://gravitytales.com', ['novel'])
    releases += links
  return releases

def rss_gravitytales():
  index = get_index()
  links = []
  for item in index:
    time.sleep(0.01)
    print "Parsing     : ", item[0]
    links += parse_feed(item[2])
  return links

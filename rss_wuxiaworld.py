#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import feedparser
import re
import urllib2
import xml.etree.ElementTree as ET
from utility_common import *


def construct_links(link_url):
  page = get_page(link_url)
  soup = BeautifulSoup(page, "lxml")
  article = soup.find('article')
  title = article.h1.text
  title = re.split(' |-', title)
  chapters = [int(str(s)) for s in title if s.isdigit()]
  links = [find_links(link_url, 'http://www.wuxiaworld.com',['index'])[0]]
  for i in xrange(chapters[0] + 1, chapters[1] + 1):
    link = links[0]
    link = link.replace(str(chapters[0]), str(i))
    links += [link]
  return links

def parse_feed():
  releases = []
  feed = feedparser.parse('http://www.wuxiaworld.com/feed/')
  for entry in feed.entries:
    link = strip_unicode(entry.link)
    links = []
    if entry.category == 'Martial God Asura':
      links = construct_links(link)
    else:
      links = find_links(link, 'http://www.wuxiaworld.com', ['index'])
    releases += links
  return releases

def rss_wuxiaworld():
    return parse_feed()

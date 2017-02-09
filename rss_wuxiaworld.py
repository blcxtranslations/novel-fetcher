#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from utility_common import *
import feedparser
import re
import urllib2
import xml.etree.ElementTree as ET


def construct_links(link_url):
  soup = BeautifulSoup(get_page(link_url), "lxml")
  article = soup.find('article')
  title = article.h1.text
  title = re.split(' |-', title)
  chapters = [int(str(s)) for s in title if s.isdigit()]
  links = [find_links(link_url, ['www.wuxiaworld.com', 'index'])[0]]
  for i in xrange(chapters[0] + 1, chapters[1] + 1):
    link = links[0]
    link = link.replace(str(chapters[0]), str(i))
    links += [link]
  return links

def parse_feed(novels):
  releases = []
  feed = feedparser.parse('http://www.wuxiaworld.com/feed/')
  for entry in feed.entries:
    if entry.category not in novels:
      continue
    link = strip_unicode(entry.link)
    links = []
    if entry.category == "Martial God Asura":
      links = construct_links(link)
    else:
      links = find_links(link, ['www.wuxiaworld.com', 'index'])
    releases += links
  return releases

def rss_wuxiaworld(novels):
  return parse_feed(novels)

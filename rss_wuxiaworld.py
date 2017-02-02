#!/usr/bin/python
# -*- coding: utf-8 -*-


import urllib2
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


novel_abbrs = [
  'DE',
  'ISSTH',
  'MGA',
]

def get_page(feed_url):
  req = urllib2.Request(feed_url , headers={'User-Agent': 'Magic Browser'})
  return urllib2.urlopen(req).read()

def find_link(link_url):
  soup = BeautifulSoup(get_page(link_url), "lxml")
  return soup.find('article').find('a')['href']

def parse_feed(feed_url):
  feed_data = get_page(feed_url)
  root = ET.fromstring(feed_data)
  links = []
  for item in root[0]:
    matched = False
    if item.tag == 'item':
      for node in item:
        if node.tag == 'title':
          for novel_abbr in novel_abbrs:
            if novel_abbr in node.text:
              matched = True
        if node.tag == 'link' and matched:
          link = find_link(node.text)
          links.append(unicode(link, 'utf-8'))
  return links

def rss_wuxiaworld():
    return parse_feed('http://www.wuxiaworld.com/feed/')

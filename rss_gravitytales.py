#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import feedparser
import re
import urllib2
import xml.etree.ElementTree as ET
from utility_common import *


novels = {
  'single': [
    "Ancient Godly Monarch",
    "Chaotic Lightning Cultivation",
  ],
  'multi': [
  ]
}


def parse_feed():
  releases = []
  feed = feedparser.parse('http://gravitytales.com/feed')
  for entry in feed.entries:
    link = strip_unicode(entry.link)
    links = []
    if any(novel in entry.title for novel in novels['single']):
      links = find_links(link, ['gravitytales.com', 'novel'])
    # elif entry.category in novels['multi']:
      # links = construct_links(link)
    releases += links
  return releases

def rss_gravitytales():
  return parse_feed()

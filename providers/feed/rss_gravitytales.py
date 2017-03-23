#!/usr/bin/python
# -*- coding: utf-8 -*-

from utilities.utility_common import *
import feedparser


def parse_feed(novels):
  releases = []
  feed = feedparser.parse('http://gravitytales.com/feed')
  for entry in feed.entries:
    link = strip_unicode(entry.link)
    links = []
    if any(novel in entry.title for novel in novels):
      links = find_links(link, ['gravitytales.com', 'novel'])
    releases += links
  return releases

def rss_gravitytales(novels):
  return parse_feed(novels)

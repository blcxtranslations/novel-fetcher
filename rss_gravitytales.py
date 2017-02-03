#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import feedparser
import re
import urllib2
import xml.etree.ElementTree as ET


novels = {
  'single': [
    "Ancient Godly Monarch",
    "Chaotic Lightning Cultivation",
  ],
  'multi': [
  ]
}


def stripunicode(text):
    return ''.join(i for i in text if ord(i)<128).strip()

def get_page(url):
  req = urllib2.Request(url , headers={'User-Agent': 'Magic Browser'})
  return urllib2.urlopen(req).read()

def find_links(link_url):
  soup = BeautifulSoup(get_page(link_url), "lxml")
  article = soup.find('article')
  links = [a['href'] for a in article.findAll('a')]
  links = filter(lambda link: 'gravitytales.com' in link and 'novel' in link, links)
  links = list(set(links))
  return links

def parse_feed():
  releases = []
  feed = feedparser.parse('http://gravitytales.com/feed')
  for entry in feed.entries:
    link = stripunicode(entry.link)
    links = []
    if any(novel in entry.title for novel in novels['single']):
      links = find_links(link)
    # elif entry.category in novels['multi']:
      # links = construct_links(link)
    releases += links
  return releases

def rss_gravitytales():
  return parse_feed()

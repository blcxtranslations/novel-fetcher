#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import feedparser
import re
import urllib2
import xml.etree.ElementTree as ET


novels = {
  'single': [
    "Desolate Era",
    "I Shall Seal the Heavens",
  ],
  'multi': [
    "Martial God Asura",
  ]
}


def stripunicode(text):
    return ''.join(i for i in text if ord(i)<128).strip()

def get_page(feed_url):
  req = urllib2.Request(feed_url , headers={'User-Agent': 'Magic Browser'})
  return urllib2.urlopen(req).read()

def find_links(link_url):
  soup = BeautifulSoup(get_page(link_url), "lxml")
  article = soup.find('article')
  links = [a['href'] for a in article.findAll('a')]
  links = filter(lambda link: 'www.wuxiaworld.com' in link and 'index' in link, links)
  links = list(set(links))
  return links

def construct_links(link_url):
  soup = BeautifulSoup(get_page(link_url), "lxml")
  article = soup.find('article')
  title = article.h1.text
  title = re.split(' |-', title)
  chapters = [int(str(s)) for s in title if s.isdigit()]
  links = [find_links(link_url)[0]]
  for i in xrange(chapters[0] + 1, chapters[1] + 1):
    link = links[0]
    link = link.replace(str(chapters[0]), str(i))
    links += [link]
  return links

def parse_feed():
  releases = []
  feed = feedparser.parse('http://www.wuxiaworld.com/feed/')
  for entry in feed.entries:
    link = stripunicode(entry.link)
    links = []
    if entry.category in novels['single']:
      links = find_links(link)
    elif entry.category in novels['multi']:
      links = construct_links(link)
    releases += links
  return releases

def rss_wuxiaworld():
    return parse_feed()

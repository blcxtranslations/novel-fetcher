#!/usr/bin/python
# -*- coding: utf-8 -*-

from rss_gravitytales import rss_gravitytales
from rss_wuxiaworld import rss_wuxiaworld
from multiprocessing import Pool
from multiprocessing import Manager
import index_gravitytales
import index_wuxiaworld
from functools import partial
import time
import feedparser
from utility_common import *
import re


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

def parse_feed(feed_url):
  releases = []
  feed = feedparser.parse(feed_url)
  for entry in feed.entries:
    link = strip_unicode(entry.link)

    links = []
    if(feed_url.startswith('http://gravitytales.com')):
      links = find_links(link, 'http://gravitytales.com', ['novel'])
    if(feed_url.startswith('http://www.wuxiaworld.com')):
      if entry.category == 'Martial God Asura':
        links = construct_links(link)
      else:
        links = find_links(link, 'http://www.wuxiaworld.com', ['index'])
    releases += links

  return releases

def fetch_rss(lock, feed):
  lock.acquire()
  print "Parsing     : ", feed
  lock.release()
  links = parse_feed(feed)
  return links

def fetch():
  gt = index_gravitytales.get_index()
  gt = [item[2] for item in gt]
  ww = index_wuxiaworld.get_index()
  ww = [item[2] for item in ww]
  feeds = list(set(gt + ww))
  feeds.sort()

  pool = Pool(len(feeds))
  manager = Manager()
  lock = manager.Lock()
  func = partial(fetch_rss, lock)
  links = pool.map(func, feeds)
  pool.close()
  pool.join()

  links = [x for sublist in links for x in sublist]
  return links

#!/usr/bin/python
# -*- coding: utf-8 -*-

from feed import Feed
from utilities.utility_common import *


class Feed_WW(Feed):
  def __init__(self):
    Feed.__init__(self)
    self.feed_url = 'http://www.wuxiaworld.com/feed/'

  def get(self, novels):
    import feedparser

    releases = []
    feed = feedparser.parse(self.feed_url)
    for entry in feed.entries:
      if entry.category not in novels:
        continue
      link = strip_unicode(entry.link)
      links = []
      if entry.category == "Martial God Asura":
        links = _construct_links(link)
      else:
        links = find_links(link, ['www.wuxiaworld.com', 'index', 'chapter'])
      releases += links
    return releases

  def _construct_links(link_url):
    from bs4 import BeautifulSoup
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

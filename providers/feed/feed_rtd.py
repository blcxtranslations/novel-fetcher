#!/usr/bin/python
# -*- coding: utf-8 -*-

from providers.feed.feed import Feed


class FeedRTD(Feed):
    def __init__(self):
        Feed.__init__(self)
        self.domain = 'http://raisingthedead.ninja/'
        self.feed_url = 'http://raisingthedead.ninja/feed/'

    def _construct_links(self, link_url):
        import re
        from bs4 import BeautifulSoup
        from utilities.utility_common import get_page, find_links

        soup = BeautifulSoup(get_page(link_url), "lxml")
        article = soup.find('article')
        title = article.h1.text
        title = re.split(' |-', title)
        chapters = [int(str(s)) for s in title if s.isdigit()]
        links = [find_links(link_url, [self.domain, 'index'])[0]]
        for i in xrange(chapters[0] + 1, chapters[1] + 1):
            link = links[0]
            link = link.replace(str(chapters[0]), str(i))
            links += [link]
        return links

    def get(self):
        import feedparser
        from utilities.utility_common import strip_unicode, find_links

        releases = []
        feed = feedparser.parse(self.feed_url)
        for entry in feed.entries:
            title = strip_unicode(entry.title)
            links = [strip_unicode(entry.link)]
            # links = find_links(entry.link, [self.domain, 'chapter'], ['#comment', '#respond', 'redirect_to'])
            releases.append((title, links))

        return releases

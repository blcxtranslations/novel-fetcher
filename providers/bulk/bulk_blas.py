#!/usr/bin/python
# -*- coding: utf-8 -*-

from providers.bulk.bulk import Bulk


def sort_links(links):
    import re

    new_links = []
    count = 0
    for link in links:
        slink = re.split('-|/', link)
        chapter = [int(str(s)) for s in slink if s.isdigit()]
        if len(chapter) > count:
            count = len(chapter)
        new_links.append([chapter, link])

    for i in xrange(count):
        new_links.sort(key=lambda x: x[0][count - 1 - i])

    new_links = [link[1] for link in new_links]
    return new_links


class BulkBLAS(Bulk):
    def __init__(self):
        Bulk.__init__(self)
        self.domain = 'http://blastron01.tumblr.com'
        self.main_url = 'http://blastron01.tumblr.com/kumoko-contents'

    def _fetch_novels(self):
        from bs4 import BeautifulSoup
        from utilities.utility_common import get_page
        from utilities.utility_common import strip_unicode

        main_page = get_page(self.main_url)
        soup = BeautifulSoup(main_page, 'lxml')
        items = soup.find('nav').findAll('a')
        items = [item for item in items if 'index' in item['href']]
        links = []
        for item in items:
            title = str(strip_unicode(item.text)).replace(' ()', '')
            link = item['href']
            links.append([title, link])
        links.sort()
        return links

    def _fetch_index(self, url):
        from utilities.utility_common import find_links

        links = find_links(url, [self.domain, 'post'])
        links = sort_links(links)
        return links

    def get(self):
        from utilities.utility_common import ask_for_index
        from utilities.utility_common import bulk_print
        from utilities.utility_common import get_common_prefix_len

        novel = 'Kumo Desu Ga, Nani Ka?'
        index = self._fetch_index(self.main_url)

        prefix_len = get_common_prefix_len(index)
        short_form = [link[prefix_len:] for link in index]
        short_form = [link[:-1] for link in short_form if link.endswith('/')] + [link for link in short_form if not link.endswith('/')]

        print "There are %s chapters in %s" % (len(index), novel)
        bulk_print(short_form)
        lower = ask_for_index("Start from chapter: ", len(index))
        upper = ask_for_index("End at chapter: ", len(index))
        index = index[lower:upper]
        return (novel, index)

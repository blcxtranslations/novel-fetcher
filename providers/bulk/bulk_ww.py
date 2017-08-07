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

def get_common_prefix(links):
    prefix = ''
    index = 0
    while True:
        index += 1
        prefix = links[0][:index]
        for link in links:
            if prefix not in link:
                if index > 0:
                    index -= 1
                return index
    return 0

class BulkWW(Bulk):
    def __init__(self):
        Bulk.__init__(self)
        self.domain = 'www.wuxiaworld.com'
        self.main_url = 'http://www.wuxiaworld.com/'

    def _fetch_novels(self):
        from bs4 import BeautifulSoup
        from utilities.utility_common import strip_unicode, get_page

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

        links = find_links(url, [self.domain, 'index', 'chapter'])
        links = sort_links(links)
        return links

    def get(self):
        from utilities.utility_common import ask_for_index, bulk_print

        novels = self._fetch_novels()

        selection_question = 'Select the novel:\n'
        for index, (novel, url) in enumerate(novels):
            selection_question += str(index + 1) + ':\t' + novel + '\n'
        selection = ask_for_index(selection_question, len(novels))

        (novel, url) = novels[selection]
        index = self._fetch_index(url)

        prefix = get_common_prefix(index)
        short_form = [link[prefix:] for link in index]
        short_form = [link[:-1] for link in short_form if link.endswith('/')] + [link for link in short_form if not link.endswith('/')]

        for link in short_form:
            print link

        print "There are %s chapters in %s" % (len(index), novels[selection][0])
        bulk_print(short_form)
        lower = ask_for_index("Start from chapter: ", len(index))
        upper = ask_for_index("End at chapter: ", len(index))
        index = index[lower:upper]
        return (novel, index)

#!/usr/bin/python
# -*- coding: utf-8 -*-

from providers.bulk.bulk import Bulk


class BulkKC(Bulk):
    def __init__(self):
        Bulk.__init__(self)
        self.domain = 'http://kobatochan.com/'
        self.main_url = 'https://kobatochan.com/'

    def _fetch_novels(self):
        from bs4 import BeautifulSoup
        from utilities.utility_common import get_page
        from utilities.utility_common import strip_unicode

        main_page = get_page(self.main_url)
        soup = BeautifulSoup(main_page, 'lxml')
        items = soup.find('nav').findAll('a')
        items = [item for item in items if 'novels' in item['href']]
        links = []
        for item in items:
            title = str(strip_unicode(item.text)).replace(' ()', '')
            link = item['href']
            links.append([title, link])
        links.sort()
        return links

    def _fetch_index(self, url):
        from utilities.utility_common import find_links
        from utilities.utility_common import sort_links

        links = []
        links += find_links(url, [self.main_url, 'chapter'])
        links += find_links(url, [self.domain, 'chapter'])
        links = sort_links(links)
        return links

    def get(self):
        from utilities.utility_common import ask_for_index
        from utilities.utility_common import bulk_print
        from utilities.utility_common import get_common_prefix_len
        from utilities.utility_common import is_number
        from utilities.utility_common import stringify_chapter_numbers

        novels = self._fetch_novels()

        selection_question = 'Select the novel:\n'
        for index, (novel, url) in enumerate(novels):
            selection_question += str(index + 1) + ':\t' + novel + '\n'
        selection = ask_for_index(selection_question, len(novels))

        (novel, url) = novels[selection]
        index = self._fetch_index(url)

        new_index = []
        for item in index:
            item = str(item)
            print item
            if 'https' in item:
                item = 'http' + item[5:]
            new_index.append(item)
        index = new_index

        prefix_len = get_common_prefix_len(index)
        short_form = [link[prefix_len:] for link in index]
        short_form = [link[:-1] for link in short_form if link.endswith('/')] + [link for link in short_form if not link.endswith('/')]

        numbers = []
        others = []
        for item in short_form:
            if is_number(item):
                numbers.append(item)
            else:
                others.append(item)

        short_form = stringify_chapter_numbers(numbers)
        short_form.sort()
        short_form += others

        print "There are %s chapters in %s" % (len(index), novels[selection][0])
        bulk_print(short_form)
        lower = ask_for_index("Start from chapter: ", len(index))
        upper = ask_for_index("End at chapter: ", len(index))
        index = index[lower:upper]
        return (novel, index)

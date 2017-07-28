#!/usr/bin/python
# -*- coding: utf-8 -*-


def ask_for_index(string, end, start=1):
    selection = -1
    while selection < start or selection > end:
        selection = raw_input(string)
        if len(selection) == 0:
            return None
        selection = int(selection)
    return selection - 1

def strip_unicode(text):
    return ''.join(i for i in text if ord(i) < 128).strip()

def get_page(url, mercury_api=None, backoff=0):
    import urllib2

    headers = {'User-Agent': 'Magic Browser'}
    if mercury_api:
        headers['x-api-key'] = mercury_api
    req = urllib2.Request(url, headers=headers)
    try:
        req = urllib2.urlopen(req)
    except urllib2.HTTPError, err:
        if err.code == 500:
            print_colour('urllib2', 'Failed', "Getting the webpage failed", 'error')
            if backoff == 3:
                raise
            print_colour('urllib2', 'Failed', "Retry number " + str(backoff), 'error')
            import time
            time.sleep(60 * pow(2, backoff))
            return get_page(url, mercury_api, backoff + 1)
    except:
        raise
    page = req.read()
    req.close()
    return page

def find_links(link_url, includes, excludes=[]):
    from lxml import html

    page = get_page(link_url)
    tree = html.fromstring(page)
    links = tree.xpath('//a/@href')
    for include in includes:
        links = [link for link in links if include in link]
    for exclude in excludes:
        links = [link for link in links if exclude not in link]
    links = list(set(links))
    return links

def send_link(reader, service, link, folder_id, mercury_api):
    if reader == 'Instapaper':
        from readers.instapaper import send_instapaper
        return send_instapaper(service, link, folder_id, mercury_api)

def print_colour(service, status, message, level=''):
    import datetime
    import time

    background = 43
    if level == 'success':
        background = 42
    elif level == 'error':
        background = 41
    elif level == 'info':
        background = 44

    totaltime = int(time.time() - time.mktime(time.localtime(0)))
    timestamp = str(datetime.datetime.fromtimestamp(totaltime))

    format_timestamp = ';'.join([str(5), str(30), str(45)])
    format_service = ';'.join([str(5), str(30), str(background)])

    text_timestamp = '{:19}'.format(timestamp)
    text_service = '{:10}'.format(service) + ': ' + '{:11}'.format(status)

    text_timestamp = '\x1b[%sm %s \x1b[0m' % (format_timestamp, text_timestamp)
    text_service = '\x1b[%sm %s \x1b[0m' % (format_service, text_service)
    print text_timestamp, text_service, message

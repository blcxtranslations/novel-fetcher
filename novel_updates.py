#!/usr/bin/python
# -*- coding: utf-8 -*-


import argparse
import time

from utilities.utility_common import send_link
from utilities.utility_database import check_links, store_link
from utilities.utility_prefs import get_prefs

import providers.fetch_rss as fetch_rss
# import providers.fetch_web as fetch_web


# def bulk(args):
#     (novels, mercury, reader) = get_prefs()
#     links = []
#     links = fetch_web.fetch()
#     links.sort()
#     send_links(links, service)

def feed(args):
    ############################################################
    from apis.instapaper import Instapaper
    ############################################################
    # print_colour('Updater', 'Checking', 'Checking for updates', level='info')

    service = None
    (novels, mercury, reader) = get_prefs()

    if reader['name'] == 'Instapaper':
        service = Instapaper(reader['key'], reader['secret'])
        service.login(reader['email'], reader['password'])

    releases = fetch_rss.fetch()
    for novel in novels:
        folder = None
        if 'folder' in novel:
            folder = novel['folder']
        for (title, links) in releases:
            if novel['name'] == title:
                links = check_links(links)
                links.sort()
                if not args.dry_run:
                    for link in links:
                        result = send_link(reader['name'], service, link, \
                            folder, mercury)
                        if result:
                            store_link(link, args.dry_run)

def daemonize(args):
    while True:
        feed(args)
        time.sleep((int)(args.interval))

def fetch(args):
    # if args.bulk:
    #     bulk(args)
    #     return
    if args.dry_run:
        feed(args)
        return
    daemonize(args)


PARSER = argparse.ArgumentParser(description='Novel Updater')
PARSER.add_argument('-b', '--bulk', dest='bulk', action='store_true', \
    help='Fetch novels in bulk')
PARSER.add_argument('-d', '--dry-run', dest='dry_run', action='store_true', \
    help='Do a dry-run, not storing, no sending to email')
PARSER.add_argument('-i', '--interval', dest='interval', default=600, \
    help='How often in seconds to check the RSS feed (default 600 seconds)')

ARGUMENTS = PARSER.parse_args()
fetch(ARGUMENTS)

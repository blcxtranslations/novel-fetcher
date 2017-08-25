#!/usr/bin/python
# -*- coding: utf-8 -*-


import argparse
import time

from utilities.utility_common import print_colour
from utilities.utility_common import send_link
from utilities.utility_database import check_links
from utilities.utility_database import store_link
from utilities.utility_prefs import get_prefs

import providers.fetch_feed as fetch_feed
import providers.fetch_bulk as fetch_bulk


def service_login(args, reader):
    service = None
    if not args.dry_run:

        if reader['name'] == 'Instapaper':
            ############################################################
            from apis.instapaper import Instapaper
            ############################################################
            service = Instapaper(reader['key'], reader['secret'])
            service.login(reader['email'], reader['password'])

    return service

def bulk(args, service, mercury, reader):
    (folder, links) = fetch_bulk.fetch()
    links = check_links(links)

    if args.dry_run:
        for link in links:
            print_colour(reader['name'], 'Would Save', link, 'success')
            print_colour('Database', 'Would Store', link, 'success')
        return

    folder_id = service.container_find_or_create(folder)
    for link in links:
        result = send_link(reader['name'], service, link, folder_id, mercury)
        if result:
            store_link(link)

def feed_worker(args, service, novels, mercury, reader):
    releases = fetch_feed.fetch()
    for novel in novels:
        print_colour('Checking', 'Novel Name', novel['name'].upper(), 'debug')

        folder = None
        if 'folder' in novel:
            folder = novel['folder']

        links_to_store = []
        for (title, links) in releases:
            if novel['name'].lower() in title.lower():
                links = check_links(links)
                # links.sort()
                links_to_store += links
        links_to_store.sort()
        if len(links_to_store) == 0:
            continue

        if args.dry_run:
            for link in links_to_store:
                print_colour(reader['name'], 'Would Save', link, 'success')
                print_colour('Database', 'Would Store', link, 'success')
            continue

        folder_id = None
        if folder:
            folder_id = service.container_find_or_create(folder)
        for link in links_to_store:
            result = send_link(reader['name'], service, link, folder_id, mercury)
            if result:
                store_link(link)

def feed(args, service, novels, mercury, reader):
    while True:
        feed_worker(args, service, novels, mercury, reader)
        if args.dry_run:
            return
        time.sleep((int)(args.interval))

def fetch(args):
    (novels, mercury, reader) = get_prefs()

    service = service_login(args, reader)
    if args.bulk:
        bulk(args, service, mercury, reader)
    else:
        feed(args, service, novels, mercury, reader)


PARSER = argparse.ArgumentParser(description='Novel Updater')
PARSER.add_argument('-b', '--bulk', dest='bulk', action='store_true', \
    help='Fetch novels in bulk')
PARSER.add_argument('-d', '--dry-run', dest='dry_run', action='store_true', \
    help='Do a dry-run, not storing, no sending to email')
PARSER.add_argument('-i', '--interval', dest='interval', default=600, \
    help='How often in seconds to check the updates feed (default 600 seconds)')

ARGUMENTS = PARSER.parse_args()
fetch(ARGUMENTS)

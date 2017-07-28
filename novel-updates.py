#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import time

from utilities.utility_common import send_link
from utilities.utility_database import *
from utilities.utility_prefs import get_prefs
import utilities.utility_settings as utility_settings

import providers.fetch_rss as fetch_rss
import providers.fetch_web as fetch_web


def fetch(args):
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
            result = send_link(reader['name'], service, link, folder, mercury)
            if result:
              store_link(link, args.dry_run)

def check_tick(args):
  if args.dry_run:
    fetch(args)
    return

  while True:
    fetch(args)
    time.sleep((int)(args.interval))

def daemonize(args):
  check_tick(args)


parser = argparse.ArgumentParser(description='Novel Updater')
parser.add_argument('-d', '--dry-run', dest='dry_run', action='store_true', help='Do a dry-run, not storing, no sending to email')
parser.add_argument('-i', '--interval', dest='interval', default=600, help='How often in seconds to check the RSS feed (default 600 seconds)')

args = parser.parse_args()
utility_settings.init()
daemonize(args)

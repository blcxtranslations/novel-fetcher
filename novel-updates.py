#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import time

from utilities.utility_common import send_links
from utilities.utility_common import send_links
from utilities.utility_database import *
from utilities.utility_prefs import get_prefs
import utilities.utility_settings as utility_settings

import providers.fetch_rss as fetch_rss
import providers.fetch_web as fetch_web


def fetch(args):
  print_colour('Updater', 'Checking', 'Checking for updates', level='info')
  (novels, service, s) = get_prefs()
  links = []
  links = fetch_rss.fetch(novels)
  links = check_links(links)
  links.sort()
  if not args.dry_run:
    send_links(links, service)
  store_links(links, args)

def check_tick(args):
  if args.dry_run:
    fetch(args)
    return

  while True:
    fetch(args)
    time.sleep((int)(args.interval))

def daemonize(args):
  check_tick(args)


parser = argparse.ArgumentParser(description='Novel Updaters')
parser.add_argument('-d', '--dry-run', dest='dry_run', action='store_true', help='Do a dry-run, not storing, no sending to email')
parser.add_argument('-i', '--interval', dest='interval', default=600, help='How often in seconds to check the RSS feed (default 600 seconds)')
parser.add_argument('-l', '--log-level', dest='loglevel', default=1, help='Level of logging messages to display')

args = parser.parse_args()
utility_settings.init()
utility_settings.loglevel = args.loglevel
daemonize(args)

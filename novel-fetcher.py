#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import time

from utility_common import send_links
from utility_database import *
from utility_prefs import get_prefs
import utility_settings

import fetch_rss
import fetch_web


def fetch(args):
  (novels, service, s) = get_prefs(args.prefs)
  links = []
  if args.fetch_new:
    links = fetch_rss.fetch(novels)
  else:
    links = fetch_web.fetch()
  links = check_links(links)
  links.sort()
  if not args.dry_run:
    send_links(links, service)
  store_links(links, args)

def check_tick(args):
  if args.fetch_new and not args.run_once:
    while True:
      fetch(args)
      time.sleep((int)(args.interval))
  else:
    fetch(args)

def daemonize(args):
  check_tick(args)


parser = argparse.ArgumentParser(description='Send links to Instapaper through GMail')
parser.add_argument('-d', '--dry-run', dest='dry_run', action='store_true', help='Do a dry-run, not storing, no sending to email')
parser.add_argument('-i', '--interval', dest='interval', default=600, help='How often in seconds to check the RSS feed (default 600 seconds)')
parser.add_argument('-l', '--log-level', dest='loglevel', default=0, help='Level of logging messages to display')
parser.add_argument('-n', '--new', dest='fetch_new', action='store_true', help='Fetch all new novels that are in the rss feed')
parser.add_argument('-o', '--run-once', dest='run_once', action='store_true', help='Run once')
parser.add_argument('-p', '--prefs', dest='prefs', help='Configuration file with email address, password, and receiver email')

args = parser.parse_args()
utility_settings.init()
utility_settings.loglevel = args.loglevel
daemonize(args)

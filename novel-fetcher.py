#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import time

from utility_database import *
from utility_email import send_links

import fetch_rss
import fetch_web


def fetch(args):
  links = []
  if args.fetch_new:
    links = fetch_rss.fetch()
  else:
    links = fetch_web.fetch()

  links = check_links(links)
  if not args.dry_run:
    send_links(links, args.config_file)
  store_links(links, args)

def check_tick(args):
  if args.dry_run or args.run_once:
    fetch(args)
  else:
    if args.fetch_new:
      while True:
        fetch(args)
        time.sleep((int)(args.interval))

def daemonize(args):
  check_tick(args)


parser = argparse.ArgumentParser(description='Send links to Instapaper through GMail')
parser.add_argument('-c', '--config', dest='config_file', help='Configuration file with email address, password, and receiver email')
parser.add_argument('-d', '--dry-run', dest='dry_run', action='store_true', help='Do a dry-run, not storing, no sending to email')
parser.add_argument('-o', '--run-once', dest='run_once', action='store_true', help='Run once')
parser.add_argument('-i', '--interval', dest='interval', default=600, help='How often in seconds to check the RSS feed (default 600 seconds)')
parser.add_argument('-n', '--new', dest='fetch_new', action='store_true', help='Fetch all new novels that are in the rss feed')

args = parser.parse_args()
daemonize(args)

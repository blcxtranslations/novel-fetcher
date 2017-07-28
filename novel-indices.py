#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import time

from utilities.utility_common import send_links
from utilities.utility_database import *
from utilities.utility_prefs import get_prefs
import utilities.utility_settings as utility_settings

import providers.fetch_rss as fetch_rss
import providers.fetch_web as fetch_web


def fetch(args):
  (n, service, s) = get_prefs()
  links = []
  links = fetch_web.fetch()
  links.sort()
  send_links(links, service)

parser = argparse.ArgumentParser(description='Send links to Instapaper through GMail')
parser.add_argument('-d', '--dry-run', dest='dry_run', action='store_true', help='Do a dry-run, not storing, no sending to email')
parser.add_argument('-l', '--log-level', dest='loglevel', default=0, help='Level of logging messages to display')

args = parser.parse_args()
utility_settings.init()
utility_settings.loglevel = args.loglevel
fetch(args)

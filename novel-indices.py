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
  (n, service, s) = get_prefs(args.prefs)
  links = []
  links = fetch_web.fetch()
  links.sort()
  send_links(links, service)

parser = argparse.ArgumentParser(description='Send links to Instapaper through GMail')
parser.add_argument('-d', '--dry-run', dest='dry_run', action='store_true', help='Do a dry-run, not storing, no sending to email')
parser.add_argument('-l', '--log-level', dest='loglevel', default=0, help='Level of logging messages to display')
parser.add_argument('-p', '--prefs', dest='prefs', help='Configuration file with email address, password, and receiver email')

args = parser.parse_args()
utility_settings.init()
utility_settings.loglevel = args.loglevel
fetch(args)

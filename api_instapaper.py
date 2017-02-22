#!/usr/bin/python
# -*- coding: utf-8 -*-

from instapaperlib import Instapaper
import urllib2


def send_instapaper(links, creds):
  from utility_common import colour_print
  if len(links) == 0:
    return
  ip = Instapaper(creds['email'], creds['password'])
  ip.auth()
  for link in links:
    (status, msg) = ip.add_item(link)
    if status == 201:
      colour_print('Stored', link, 'success')
    else:
      colour_print('Failed', link, 'error')

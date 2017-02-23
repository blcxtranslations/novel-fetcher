#!/usr/bin/python
# -*- coding: utf-8 -*-

from instapaperlib import Instapaper
import urllib2


def send_instapaper(links, creds):
  from utility_common import print_colour
  if len(links) == 0:
    return
  ip = Instapaper(creds['email'], creds['password'])
  ip.auth()
  for link in links:
    (status, msg) = ip.add_item(link)
    if status == 201:
      print_colour('Instapaper', 'Success', link, 'success')
    else:
      print_colour('Instapaper', 'Failed', link, 'error')

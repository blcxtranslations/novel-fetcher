#!/usr/bin/python
# -*- coding: utf-8 -*-

from instapaperlib import Instapaper
import urllib2


def send_instapaper(links, creds):
  if len(links) == 0:
    return
  ip = Instapaper(creds['email'], creds['password'])
  ip.auth()
  for link in links:
    (status, msg) = ip.add_item(link)
    if status == 201:
      print "Stored      : ", link
    else:
      print "Failed      : ", link

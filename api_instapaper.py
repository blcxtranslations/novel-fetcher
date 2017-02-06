#!/usr/bin/python
# -*- coding: utf-8 -*-

from utility_common import *
import urllib2
from instapaperlib import Instapaper


def get_creds(creds):
  f = open(creds)
  username = f.readline()[:-1]
  password = f.readline()[:-1]
  f.close()
  return username, password

def send_instapaper(links, creds):
  if len(links) == 0:
    return

  username, password = get_creds(creds)

  ip = Instapaper(username, password)
  ip.auth()

  for link in links:
    (status, msg) = ip.add_item(link)
    if status == 201:
      print "Stored      : ", link
    else:
      print "Failed      : ", link

#!/usr/bin/python
# -*- coding: utf-8 -*-

from apis.instapaper import Instapaper
import urllib2


def send_instapaper(links, creds):
  # Circular dependency requires that we only import this
  # And only import it inside this function
  ############################################################
  from utilities.utility_common import print_colour
  ############################################################

  if len(links) == 0:
    return
  ip = Instapaper(creds['key'], creds['secret'])
  ip.login(creds['email'], creds['password'])
  for link in links:
    success, msg = ip.bookmark_add(link)
    if success:
      print_colour('Instapaper', 'Success', link, 'success')
    else:
      print_colour('Instapaper', 'Failed', link, 'error')

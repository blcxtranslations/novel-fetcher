#!/usr/bin/python
# -*- coding: utf-8 -*-

from feed.feed_ww import Feed_WW


def fetch():
  feed_ww = Feed_WW()
  releases = []
  releases += feed_ww.get()
  return releases

#!/usr/bin/python
# -*- coding: utf-8 -*-

from feed.feed_ww import Feed_WW


def fetch(novels):
  feed_ww = Feed_WW()
  links = []
  links += feed_ww.get(novels)
  return links

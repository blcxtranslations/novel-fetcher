#!/usr/bin/python
# -*- coding: utf-8 -*-

from feed.rss_wuxiaworld import rss_wuxiaworld


def fetch(novels):
  links = []
  links += rss_wuxiaworld(novels)
  return links

#!/usr/bin/python
# -*- coding: utf-8 -*-

from feed.rss_gravitytales import rss_gravitytales
from feed.rss_wuxiaworld import rss_wuxiaworld


def fetch(novels):
  links = []
  links += rss_gravitytales(novels)
  links += rss_wuxiaworld(novels)
  return links

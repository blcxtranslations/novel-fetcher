#!/usr/bin/python
# -*- coding: utf-8 -*-

from rss_gravitytales import rss_gravitytales
from rss_wuxiaworld import rss_wuxiaworld


def fetch():
  links = []
  links += rss_gravitytales()
  links += rss_wuxiaworld()
  return links

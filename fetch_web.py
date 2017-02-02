#!/usr/bin/python
# -*- coding: utf-8 -*-

from web_gravitytales import web_gravitytales
from web_wuxiaworld import web_wuxiaworld


def fetch():
  links = []
  links += web_gravitytales()
  links += web_wuxiaworld()
  return links

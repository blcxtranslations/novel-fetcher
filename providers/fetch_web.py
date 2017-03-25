#!/usr/bin/python
# -*- coding: utf-8 -*-

from bulk.web_wuxiaworld import web_wuxiaworld


def ask_for_index(str, end, start=1):
  selection = -1
  while selection < start or selection > end:
    selection = raw_input(str)
    if len(selection) == 0:
      return None
    selection = int(selection)
  return selection - 1

def fetch():
  return web_wuxiaworld()

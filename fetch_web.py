#!/usr/bin/python
# -*- coding: utf-8 -*-

from web_gravitytales import web_gravitytales
from web_wuxiaworld import web_wuxiaworld


def ask_for_index(str, end, start=1):
  selection = -1
  while selection < start or selection > end:
    selection = raw_input(str)
    if len(selection) == 0:
      return None
    selection = int(selection)
  return selection - 1

def fetch():
  selection = ask_for_index('1 for gravitytales, 2 for wuxiaworld : ', 2)
  if selection == 1:
    return web_wuxiaworld()
  else:
    return web_gravitytales()

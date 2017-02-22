#!/usr/bin/python
# -*- coding: utf-8 -*-

from utility_common import colour_print
import sqlite3


def check_links(links):
  conn = sqlite3.connect('novels.db')
  conn.cursor().execute("CREATE TABLE IF NOT EXISTS chapters (link varchar(256))")
  conn.commit()
  c = conn.cursor()

  newlinks = []
  for link in links:
    colour_print('Searching', link)
    c.execute("SELECT * FROM chapters WHERE link='" + link + "'")
    if not c.fetchone():
      colour_print('New Link', link)
      newlinks.append(link)
    else:
      colour_print('Old Link', link)

  conn.close()
  return newlinks

def store_links(links, args):
  conn = sqlite3.connect('novels.db')

  for link in links:
    if not args.dry_run:
      c = conn.cursor()
      c.execute("INSERT INTO chapters (link) VALUES ('" + link + "')")
      colour_print('Store Link', link, 'success')
    else:
      colour_print('Would Link', link, 'success')
  conn.commit()
  conn.close()

  return links

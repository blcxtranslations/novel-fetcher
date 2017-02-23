#!/usr/bin/python
# -*- coding: utf-8 -*-

from utility_common import print_colour
import sqlite3


def check_links(links):
  conn = sqlite3.connect('novels.db')
  conn.cursor().execute("CREATE TABLE IF NOT EXISTS chapters (link varchar(256))")
  conn.commit()
  c = conn.cursor()

  newlinks = []
  for link in links:
    print_colour('DB', 'Search', link)
    c.execute("SELECT * FROM chapters WHERE link='" + link + "'")
    if not c.fetchone():
      print_colour('DB', 'New Link', link)
      newlinks.append(link)
    else:
      print_colour('DB', 'Old Link', link)

  conn.close()
  return newlinks

def store_links(links, args):
  conn = sqlite3.connect('novels.db')

  for link in links:
    if not args.dry_run:
      c = conn.cursor()
      c.execute("INSERT INTO chapters (link) VALUES ('" + link + "')")
      print_colour('DB', 'Stored', link, 'success')
    else:
      print_colour('DB', 'Would Store', link, 'success')
  conn.commit()
  conn.close()

  return links

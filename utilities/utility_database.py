#!/usr/bin/python
# -*- coding: utf-8 -*-

from utility_common import print_colour
import sqlite3


def check_links(links):
  conn = sqlite3.connect('configs/novels.db')
  conn.cursor().execute("CREATE TABLE IF NOT EXISTS chapters (link varchar(256))")
  conn.commit()
  c = conn.cursor()

  newlinks = []
  for link in links:
    c.execute("SELECT * FROM chapters WHERE link='" + link + "'")
    if not c.fetchone():
      print_colour('Database', 'New Link', link)
      newlinks.append(link)
    else:
      print_colour('Database', 'Old Link', link)

  conn.close()
  return newlinks

def store_link(link, dry_run=True):
  conn = sqlite3.connect('configs/novels.db')
  if dry_run:
    print_colour('Database', 'Would Store', link, 'success')
  else:
    c = conn.cursor()
    c.execute("INSERT INTO chapters (link) VALUES ('" + link + "')")
    print_colour('Database', 'Stored', link, 'success')
  conn.commit()
  conn.close()

#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3


def check_links(links):
  conn = sqlite3.connect('novels.db')
  conn.cursor().execute("CREATE TABLE IF NOT EXISTS chapters (link varchar(256))")
  conn.commit()
  c = conn.cursor()

  newlinks = []
  oldlinks = []
  print '=' * 80
  for link in links:
    print "Found       : ", link
    c.execute("SELECT * FROM chapters WHERE link='" + link + "'")
    if not c.fetchone():
      newlinks.append(link)
    else:
      oldlinks.append(link)
  conn.close()

  print '=' * 80
  for link in newlinks:
    print "New Link    : ", link
  print '=' * 80
  for link in oldlinks:
      print "Old Link    : ", link
  print '=' * 80

  return newlinks

def store_links(links, args):
  conn = sqlite3.connect('novels.db')

  for link in links:
    if not args.dry_run:
      c = conn.cursor()
      c.execute("INSERT INTO chapters (link) VALUES ('" + link + "')")
      print "Stored Link : ", link
    else:
      print "Would Store : ", link
  conn.commit()
  conn.close()

  return links

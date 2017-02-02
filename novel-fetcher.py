#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from email.mime.text import MIMEText
import argparse
import smtplib
import sqlite3
import time
import urllib2
import xml.etree.ElementTree as ET


novel_abbrs = [
  'BTTH',
  'DE',
  'ISSTH',
  'MGA',
  'TDG',
  'TGR',
  'WDQK',
]


def get_page(feed_url):
  req = urllib2.Request(feed_url , headers={'User-Agent': 'Magic Browser'})
  return urllib2.urlopen(req).read()


def find_link(link_url):
  soup = BeautifulSoup(get_page(link_url), "lxml")
  return soup.find('article').find('a')['href']


def parse_feed(feed_url):
  feed_data = get_page(feed_url)
  root = ET.fromstring(feed_data)
  links = []
  for item in root[0]:
    matched = False
    if item.tag == 'item':
      for node in item:
        if node.tag == 'title':
          for novel_abbr in novel_abbrs:
            if novel_abbr in node.text:
              matched = True
        if node.tag == 'link' and matched:
          link = find_link(node.text)
          links.append(unicode(link, 'utf-8'))
  return links


def check_links(links):
  conn = sqlite3.connect('novels.db')
  conn.cursor().execute("CREATE TABLE IF NOT EXISTS chapters (link varchar(256))")
  conn.commit()
  c = conn.cursor()

  newlinks = []
  for link in links:
    print "Searching   : ", link
    c.execute("SELECT * FROM chapters WHERE link='" + link + "'")
    if not c.fetchone():
      print "New Link    : ", link
      newlinks.append(link)
    else:
      print "Old Link    : ", link

  conn.close()
  return newlinks


def store_links(links):
  conn = sqlite3.connect('novels.db')

  for link in links:
    c = conn.cursor()
    c.execute("INSERT INTO chapters (link) VALUES ('" + link + "')")
    print "Stored Link : ", link
  conn.commit()
  conn.close()

  return links


def send_links(username, password, receiver, links):
  if len(links) == 0:
    return

  try:
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)
    print "Connecting  : ", username
  except:
    print "Failed      : ", username
    raise

  for link in links:
    message = MIMEText(link)
    try:
      server.sendmail(username, receiver, message.as_string())
      print "Sending     : ", link
    except:
      print "Failed      : ", link
      raise

  server.quit()


def check_feed(username, password, receiver, args):
  links = parse_feed('http://www.wuxiaworld.com/feed/')
  links = check_links(links)
  if not args.dry_run:
    send_links(username, password, receiver, links)
  store_links(links)


def check_tick(username, password, receiver, args):
  if args.dry_run:
    check_feed(username, password, receiver, args)
  else:
    while True:
      check_feed(username, password, receiver, args)
      time.sleep((int)(args.interval))


def get_creds(args):
  # TODO: more secure way of creds
  f = open(args.config_file)
  username = f.readline()[:-1]
  password = f.readline()[:-1]
  receiver = f.readline()[:-1]
  f.close()
  return username, password, receiver


def daemonize(args):
  username, password, receiver = get_creds(args)
  check_tick(username, password, receiver, args)


parser = argparse.ArgumentParser(description='Send links to Instapaper through GMail')
parser.add_argument('-c', '--config', dest='config_file', help='Configuration file with email address, password, and receiver email')
parser.add_argument('-d', '--dry-run', dest='dry_run', action='store_true', help='Do a dry-run, not storing, no sending to email')
parser.add_argument('-i', '--interval', dest='interval', default=600, help='How often in seconds to check the RSS feed (default 600 seconds)')

args = parser.parse_args()
daemonize(args)

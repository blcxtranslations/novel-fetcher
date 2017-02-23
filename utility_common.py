#!/usr/bin/python
# -*- coding: utf-8 -*-

from api_instapaper import send_instapaper
from lxml import html
import urllib2
import utility_settings


def strip_unicode(text):
    return ''.join(i for i in text if ord(i)<128).strip()

def get_page(url):
  req = urllib2.Request(url , headers={'User-Agent': 'Magic Browser'})
  req = urllib2.urlopen(req)
  page = req.read()
  req.close()
  return page

def find_links(link_url, includes, excludes=[]):
  page = get_page(link_url)
  tree = html.fromstring(page)
  links = tree.xpath('//a/@href')
  for include in includes:
    links = filter(lambda link: include in link, links)
  for exclude in excludes:
    links = filter(lambda link: exclude not in link, links)
  links = list(set(links))
  return links

def send_links(links, service):
  if service['name'] == 'Instapaper':
    send_instapaper(links, service)

def print_colour(service, status, message, level=''):
  if level not in  ['success', 'error'] and utility_settings.loglevel == 0:
    return

  background = 43
  if level == 'success':
    background = 42
  elif level == 'error':
    background = 41

  format = ';'.join([str(5), str(30), str(background)])
  text = '{:10}'.format(service) + ': ' + '{:8}'.format(status)
  text = '\x1b[%sm %s \x1b[0m' % (format, text)
  print text, message

#!/usr/bin/python
# -*- coding: utf-8 -*-

from lxml import html
import datetime
import time
import urllib2
import utility_settings


def strip_unicode(text):
    return ''.join(i for i in text if ord(i)<128).strip()

def get_page(url, mercury_api=None, backoff=0):
  headers = {'User-Agent': 'Magic Browser'}
  if mercury_api:
    headers['x-api-key'] = mercury_api
  req = urllib2.Request(url , headers=headers)
  try:
    req = urllib2.urlopen(req)
  except urllib2.HTTPError as err:
    if err.status == 500:
      print_colour('urllib2', 'Failed', "Getting the webpage failed", 'error')
      if backoff == 3:
        raise
      print_colour('urllib2', 'Failed', "Retry number " + str(backoff), 'error')
      import time
      time.sleep(60 * math.pow(2, backoff))
      return get_page(url, mercury_api, backoff + 1)
  except:
    raise
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

def send_links(service, links, folder, mercury_api):
  if service['name'] == 'Instapaper':
    from readers.instapaper import send_instapaper
    send_instapaper(service, links, folder, mercury_api)

def print_colour(service, status, message, level=''):
  if level == 'debug' and utility_settings.loglevel < 2:
    return
  if level == 'info' and utility_settings.loglevel < 1:
    return

  background = 43
  if level == 'success':
    background = 42
  elif level == 'error':
    background = 41
  elif level == 'info':
    background = 44

  totaltime = int(time.time() - time.mktime(time.localtime(0)))
  timestamp = str(datetime.datetime.fromtimestamp(totaltime))

  format_timestamp = ';'.join([str(5), str(30), str(45)])
  format_service = ';'.join([str(5), str(30), str(background)])

  text_timestamp = '{:19}'.format(timestamp)
  text_service = '{:10}'.format(service) + ': ' + '{:11}'.format(status)

  text_timestamp = '\x1b[%sm %s \x1b[0m' % (format_timestamp, text_timestamp)
  text_service = '\x1b[%sm %s \x1b[0m' % (format_service, text_service)
  print text_timestamp, text_service, message

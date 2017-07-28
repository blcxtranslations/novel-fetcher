#!/usr/bin/python
# -*- coding: utf-8 -*-

from apis.instapaper import Instapaper
import urllib2


def send_instapaper(service, link, folder_name, mercury_api):
  # Circular dependency requires that we only import this
  # And only import it inside this function
  ############################################################
  from utilities.utility_common import get_page
  from utilities.utility_common import print_colour
  import json
  ############################################################

  folder_id = None
  if folder_name:
    folder_id = service.folders_find_or_create(folder_name)

  if mercury_api:
    page = get_page('https://mercury.postlight.com/parser?url=' + link, mercury_api)
    page = json.loads(page)
    success, msg = service.bookmark_add(link, folder_id, page['content'])
  else:
    success, msg = service.bookmark_add(link, folder_id)

  if success:
    print_colour('Instapaper', 'Success', link, 'success')
    return True

  print_colour('Instapaper', 'Failed', link, 'error')
  return False

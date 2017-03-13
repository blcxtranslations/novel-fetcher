#!/usr/bin/python
# -*- coding: utf-8 -*-

import pprint
import simplejson


def get_prefs(prefs):
  # TODO: more secure way of creds
  f = open(prefs)
  conf = f.read()
  f.close()
  conf = simplejson.loads(conf)
  for s in conf['services']:
    if s['default']:
      service = s
  return conf['novels'], service, conf['services']

def update_prefs(prefs, novels):
  (n, ds, s) = get_prefs(prefs)
  new = {}
  new['services'] = s
  new['novels'] = list(set(n + novels))
  f = open(prefs, 'w')
  pjson = simplejson.dumps(new, sort_keys=True, indent=2, separators=(',', ': '))
  f.write(pjson)
  f.close()

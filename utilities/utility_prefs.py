#!/usr/bin/python
# -*- coding: utf-8 -*-

def get_prefs():
  # TODO: more secure way of creds

  from os import listdir
  import pprint
  import simplejson

  configs = [name for name in listdir('configs/') if name.endswith('conf') and name != 'sample.conf']
  if len(configs) != 1:
    print "Too many custom config files, exiting"
    exit()
  f = open('configs/' + configs[0])
  conf = f.read()
  f.close()
  conf = simplejson.loads(conf)
  for s in conf['services']:
    if s['default']:
      service = s
  return conf['novels'], service, conf['services']

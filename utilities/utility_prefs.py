#!/usr/bin/python
# -*- coding: utf-8 -*-


def get_prefs():
    from os import listdir
    import json

    # Restricting the number of config files down to one for now
    configs = [name for name in listdir('configs/') if name.endswith('conf') and name != 'sample.conf']
    if len(configs) != 1:
        print "Too many custom config files, exiting"
        exit()

    file_handle = open('configs/' + configs[0])
    conf = file_handle.read()
    file_handle.close()

    conf = json.loads(conf)

    if 'mercury_api' in conf:
        return conf['novels'], conf['mercury_api'], conf['reader']
    else:
        return conf['novels'], None, conf['reader']

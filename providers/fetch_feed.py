#!/usr/bin/python
# -*- coding: utf-8 -*-

from providers.feed.feed_ww import FeedWW


def fetch():
    feed_ww = FeedWW()
    releases = []
    releases += feed_ww.get()
    return releases

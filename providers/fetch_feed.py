#!/usr/bin/python
# -*- coding: utf-8 -*-

from providers.feed.feed_ww import FeedWW
from providers.feed.feed_kc import FeedKC


def fetch():
    feed_ww = FeedWW()
    feed_kc = FeedKC()

    releases = []
    releases += feed_ww.get()
    releases += feed_kc.get()

    return releases

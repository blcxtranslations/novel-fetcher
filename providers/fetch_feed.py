#!/usr/bin/python
# -*- coding: utf-8 -*-

from providers.feed.feed_kc import FeedKC
from providers.feed.feed_rtd import FeedRTD
from providers.feed.feed_ww import FeedWW


def fetch():
    feed_kc = FeedKC()
    feed_rtd = FeedRTD()
    feed_ww = FeedWW()

    releases = []
    releases += feed_kc.get()
    releases += feed_rtd.get()
    releases += feed_ww.get()

    return releases

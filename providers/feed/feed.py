#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABCMeta
from abc import abstractmethod


class Feed:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def get(self):
        pass

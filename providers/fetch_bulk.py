#!/usr/bin/python
# -*- coding: utf-8 -*-

from providers.bulk.bulk_ww import BulkWW
from utilities.utility_common import ask_for_index


def fetch():
    bulk_ww = BulkWW()

    selections = [
        ('Wuxiaworld', bulk_ww.get)
    ]

    selection_question = 'Select the novel site:\n'
    for index, (selection, fetch) in enumerate(selections):
        selection_question += str(index + 1) + ':\t' + selection + '\n'
    selection = ask_for_index(selection_question, len(selections))

    (selection, get) = selections[selection]
    return get()

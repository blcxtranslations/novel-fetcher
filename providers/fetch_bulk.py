#!/usr/bin/python
# -*- coding: utf-8 -*-

from utilities.utility_common import ask_for_index

from providers.bulk.bulk_blas import BulkBLAS
from providers.bulk.bulk_turbo import BulkTURBO
from providers.bulk.bulk_ww import BulkWW


def fetch():
    bulk_blas = BulkBLAS()
    bulk_turbo = BulkTURBO()
    bulk_ww = BulkWW()

    selections = [
        ('Blastron', bulk_blas.get),
        ('Turbo', bulk_turbo.get),
        ('Wuxiaworld', bulk_ww.get),
    ]

    selection_question = 'Select the novel site:\n'
    for index, (selection, get) in enumerate(selections):
        selection_question += str(index + 1) + ':\t' + selection + '\n'
    selection = ask_for_index(selection_question, len(selections))

    (selection, get) = selections[selection]
    return get()

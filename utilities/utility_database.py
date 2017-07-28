#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3

from utilities.utility_common import print_colour


def check_links(links):
    conn = sqlite3.connect('configs/novels.db')
    conn.cursor().execute("CREATE TABLE IF NOT EXISTS chapters (link varchar(256))")
    conn.commit()
    cursor = conn.cursor()

    newlinks = []
    for link in links:
        cursor.execute("SELECT * FROM chapters WHERE link='" + link + "'")
        if not cursor.fetchone():
            print_colour('Database', 'New Link', link)
            newlinks.append(link)
        else:
            print_colour('Database', 'Old Link', link)

    conn.close()
    return newlinks

def store_link(link, dry_run=True):
    conn = sqlite3.connect('configs/novels.db')
    if dry_run:
        print_colour('Database', 'Would Store', link, 'success')
    else:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO chapters (link) VALUES ('" + link + "')")
        print_colour('Database', 'Stored', link, 'success')
    conn.commit()
    conn.close()

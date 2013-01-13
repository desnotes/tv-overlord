#!/usr/bin/env python

from tvrage import feeds
import tvrage.api
from xml.etree.ElementTree import tostring
import sqlite3
from ConsoleInput import ask_user as ask


def dict_factory (cursor, row):
    '''Changes the data returned from the db from a
    tupple to a dictionary'''
    d = {}
    for idx, col in enumerate (cursor.description):
        d[col[0]] = row[idx]
    return d


db_file = '/home/sm/.nzb/shows.v2.sqlite3'
sql = "SELECT name, season, episode, thetvdb_series_id, nzbmatrix_search_name, ragetv_series_id, status \
    FROM shows ORDER BY replace (name, 'The ', '');"
conn = sqlite3.connect (db_file)
conn.row_factory = dict_factory
curs = conn.cursor()
# ddata = curs.execute(sql)
curs.execute(sql)
ddata = curs.fetchall()
for x in ddata:
    s = feeds.search(x['name'])
    rage_name = s.getchildren()[0].getchildren()[1].text
    rage_id = s.getchildren()[0].getchildren()[0].text

    print x['name'], '---', rage_name
    # print x['thetvdb_series_id'], rage_id

    #for title in s:
    #    print '    ', title.getchildren()[1].text,
    #    print '-', title.getchildren()[0].text

    # correct = ask ('Correct?')

    update_sql = 'update shows set ragetv_series_id=:ragetv_series_id where thetvdb_series_id=:thetvdb_series_id'
    update_vals = {'ragetv_series_id': rage_id, 'thetvdb_series_id': x['thetvdb_series_id']}
    curs.execute(update_sql, update_vals)
    print update_vals

print 'closing db'
conn.commit()
conn.close()

# Louie (2010) --- Louie
# Once Upon a Time (2011) --- Once Upon a Time
# Scandal (2012) --- Scandal
#

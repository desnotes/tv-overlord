#!/usr/bin/env python

import feedparser
import urllib
import os
from time import mktime
from datetime import datetime
import pprint
from Util import U


class Provider (object):
    provider_url = 'http://kickass.to/usearch/%s/?rss=1'
    name = 'Kickass Torrents'


    def search(self, search_string):

        query = search_string
        encoded_search = urllib.quote (query)
        full_url = self.provider_url % (encoded_search)
        # print full_url

        parsed = feedparser.parse(full_url)
        header = [['Name', 'Size', 'Date', 'Seeds'], [0, 10, 12, 10]]
        show_data = []

        for show in parsed['entries']:
            dt = datetime.fromtimestamp(mktime(show['published_parsed']))
            date = dt.strftime('%b %d/%Y')

            size = U.pretty_filesize (show['torrent_contentlength'])
            # size = size.replace ('GB', U.fg_color ('yellow', 'GB'))

            # title = U.snip (show['title'].ljust (title_w), title_w)
            # title = title.replace ('avi', U.fg_color ('green', 'avi'))
            title = show['title']

            show_data.append([
                title,                    # title
                size,                     # show size
                date,                     # date
                show['torrent_seeds'],    # seeds
                show['torrent_magneturi'] # id (download magnet url)
            ])

        show_data.sort(key=lambda x: int(x[3]), reverse=True) # sort by seeds
        return [header] + [show_data]

    def download (self, chosen_show, destination, final_name):

        pass


if __name__ == '__main__':

    url = 'http://kickass.to/usearch/under%20the%20dome%20category%3Atv/?rss=1'

    show = Provider()

    results = show.search ('"doctor who (2005) 5x01" OR "doctor who 2005 s05e01"')

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint (results)

    '''
    torrent_magneturi
    id
    title_detail --- {'base': u'http://kickass.to/usearch/under%20the%20dome%20category%3Atv/?rss=1', 'type': u'text/plain', 'value': u'Under the Dome S01E01 720p HDTV X264-DIMENSION [eztv]', 'language': None}
    torrent_seeds
    torrent_contentlength --- 1252895269
    title --- Under the Dome S01E01 720p HDTV X264-DIMENSION [eztv]
    published_parsed --- time.struct_time(tm_year=2013, tm_mon=6, tm_mday=25, tm_hour=5, tm_min=45, tm_sec=2, tm_wday=1, tm_yday=176, tm_isdst=0)
    torrent_infohash --- DF4708C7E96E439FADDCD6F5BCD1A79503A1738C

    "doctor who (2005) 5x01" OR "doctor who 2005 s05e01"

    '''
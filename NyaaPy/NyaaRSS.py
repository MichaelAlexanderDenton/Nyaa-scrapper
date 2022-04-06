"""
    TODO:
        ---overwrite/not existing torrent files/data
        ---Check query if user has submitted valid input
        ---Add more debug console data.
        ---if page returns empty, put an exception.
        ---category needs to be parse and converted.
        ---get files by their tier (trusted, success, not-trusted, neutral...)
"""

from DataProcess import DataProcess
import json
import requests
import re
from json import JSONDecodeError
import pprint
import string
class NyaaRSS(DataProcess):
    def __init__(self):
        super().__init__()
        
    
    def get_latest_feed_data(self, rtype='dict', limit=None):
        pp = pprint.PrettyPrinter(indent=4)
        feed_data = self._parse_rss_feed(limit=limit)
        try:
            if rtype == 'json':
                return json.dumps(feed_data)
            if rtype == 'dict':
                return feed_data
            if rtype == 'debug':
                print(f"Object type: {feed_data.__class__()}")
                pp.pprint(feed_data)
            if rtype is not ['json', 'debug', 'dict']:
                raise ValueError('Invalid value for rtype. Try again.')
        except JSONDecodeError:
            raise ('Error while parsing data to JSON notation.')
        
    def get_latest_torrent_files(self, limit=None):
        return self._rss_get_torrent_files(limit=limit)
        
        
    def get_data_by_query(self, 
                                filter_=None, 
                                search_query=None, 
                                category=None,
                                username=None,
                                limit=None):
        
        search_url = self._create_search_query(filter_=filter_, 
                                     search_query=search_query, 
                                     category=category, 
                                     username=username,
                                     search_type='rss')
        
        return self._parse_rss_feed(search_url, limit=limit)

    
    def get_torrents_by_query(self, 
                                filter_=None, 
                                search_query=None, 
                                category=None, 
                                username=None, 
                                limit=None):
        
        search_url = self._create_search_query(filter_=filter_, 
                                     search_query=search_query, 
                                     category=category, 
                                     username=username,
                                     search_type='rss')
        
        self._rss_get_torrent_files(url=search_url, limit=limit)


    def get_data_by_username(self, username=None, limit=None):
        search_url = self._create_search_query(username=username, search_type='rss')
        return self._parse_rss_feed(search_url, limit=limit)
        
    def get_torrents_by_username(self, username=None, limit=None):
        search_url = self._create_search_query(username=username, search_type='rss')
        self._rss_get_torrent_files(search_url, limit=limit)
        

rss = NyaaRSS()
rss.get_data_by_query(search_query="Digimon Adventure", category=("Anime", "English-translated"), filter_="no remake")
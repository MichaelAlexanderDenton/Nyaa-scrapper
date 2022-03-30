"""
    TODO:
        ---Don't overwrite exisiting torrent files/data
        ---Check query if user has submitted valid input
        ---Add more debug console data.
"""

from DataProcess import DataProcess
import json
import requests
import re
from json import JSONDecodeError
import pprint
import string
class NyaaRSS(DataProcess):
    def RSS_get_latest_feed_data(self, url, rtype=None, limit=None):
        feed_data = self.parse_rss_feed(url, limit=limit)
        try:
            if rtype == 'json':
                return json.dumps(feed_data)
            if rtype == 'dict':
                return feed_data
            if rtype == 'debug':
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(type(obj))
            if rtype is not ['json', 'dict', 'debug']:
                raise TypeError('Invalid type, try again. i.e --> type="dict"/type="json"')
        except JSONDecodeError:
            raise ('Invalid type, try again. i.e --> rtype="dict"/rtype="json"')
        

    def RSS_query_search_data(self, filter_type=None, query=None, category=None, username=None):
        search_url = self.RSS_create_search_query(filter_=filter_type, 
                                     search_string=query, 
                                     category=category, 
                                     username=username)
        search_feed_data = self.RSS_get_latest_feed_data(search_url, rtype='dict')
        return search_feed_data
        
    def RSS_get_query_search_torrents(self, 
                                      filter_type=None, 
                                      query=None, 
                                      category=None, 
                                      username=None, 
                                      limit=None):
        search_url = self.RSS_create_search_query(filter_=filter_type, 
                                     search_string=query, 
                                     category=category, 
                                     username=username)
        self.get_torrent_files(search_url)

    def RSS_search_data_by_username(self, username=None):
        search_url = self.RSS_create_search_query(username=username)
        return self.RSS_get_latest_feed_data(search_url)
        
    def RSS_search_torrents_by_username(self, username=None):
        search_url = self.RSS_create_search_query(username=username)
        self.get_torrent_files(search_url)
        
        
rss = NyaaRSS()
rss.RSS_get_query_search_torrents(query='Digimon adventure')
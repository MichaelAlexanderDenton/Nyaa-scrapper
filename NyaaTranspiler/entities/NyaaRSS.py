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
    def RSS_get_latest_feed_data(self, rtype=None, limit=None):
        feed_data = self.parse_rss_feed("https://nyaa.si/?page=rss&", limit=limit)
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
        
    def RSS_get_latest_torrent_files(self, limit=None):
        return self.get_torrent_files("https://nyaa.si/?page=rss&", limit=limit)
        
        
    def RSS_query_search_data(self, filter_type=None, query=None, category=None, username=None):
        search_url = self.create_search_query(filter_=filter_type, 
                                     search_string=query, 
                                     category=category, 
                                     username=username)
        print(f"Search link: {search_url}")
        return self.parse_rss_feed(search_url)

    
    def RSS_get_query_search_torrents(self, 
                                      filter_type=None, 
                                      query=None, 
                                      category=None, 
                                      username=None, 
                                      limit=None):
        search_url = self.create_search_query(filter_=filter_type, 
                                     search_string=query, 
                                     category=category, 
                                     username=username)
        self.get_torrent_files(search_url, limit=limit)


    def RSS_search_data_by_username(self, username=None):
        search_url = self.create_search_query(username=username)
        print(f"username: {username} \n search link: {search_url}")
        return self.parse_rss_feed(search_url)
        
    def RSS_get_torrents_by_username(self, username=None):
        search_url = self.create_search_query(username=username)
        print(f" username: {username}\nsearch link: {search_url}")
        self.get_torrent_files(search_url)
        
        
rss = NyaaRSS()
x = rss.RSS_get_latest_torrent_files()

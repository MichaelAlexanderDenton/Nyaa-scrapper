"""
    TODO:
        ---if page returns empty, put an exception.
        ---category needs to be parse and converted.
        ---get files by their tier (trusted, success, not-trusted, neutral...)
        ---Add an exception if the page scrapped returned nothing
"""

from bs4 import BeautifulSoup
from json import JSONDecodeError
from DataProcess import DataProcess
from collections import OrderedDict
import json
import pprint
class NyaaScraper(DataProcess):
    def __init__(self):
        self.base__url = "http://nyaa.si/"
    
    
    def _debug_show_titles(self):
        page_data = self.parse_scraper_data()
        mlist = list()
        for i in page_data['data']:
            mlist.append(i['title'])
        return mlist
    
    
    def get_latest_torrent_data(self, rtype='dict', pages=None, per_page=None):
        page_data = self.parse_scraper_data(pages=pages, per_page=per_page)
        try:
            if rtype == 'json':
                return json.dumps(page_data)
            if rtype == 'dict':
                return page_data
            if rtype == 'debug':
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(type(obj))
            if rtype is not ['json', 'dict', 'debug']:
                raise TypeError('Invalid type, try again. i.e --> type="dict"/type="json"')
        except JSONDecodeError:
            raise ('Invalid type, try again. i.e --> rtype="dict"/rtype="json"')
    
    
    def get_latest_torrent_files(self, pages=None, per_page=None):
        pages_data = self.parse_scraper_data(pages=pages, per_page=per_page)
        self.get_data(pages_data)
        
    ##########################################################
    ## search_data_by_pages was removed due to be a spammy
    ## method to use
    ## Might add later.
    ##########################################################
    
    def get_data_by_query(self, filter_=None, search_string=None, category=None, username=None, pages=None, per_page=None):
        # Maybe we can move this somewhere else...
        scraper_data = OrderedDict({
            "title" : f"Nyaa Scraper v0.1 (Under construction v0204)",
            "description": f"Nyaa scraper for {search_string}"
        })
        search_url = self.create_search_query(
            filter_=filter_, 
            search_string=search_string, 
            category=category, 
            username=username,
            search_type="scraper")
        print(f"Search link: {search_url}")
        return self.parse_scraper_data(url=search_url, pages=pages, per_page=per_page)
    
    def get_torrent_files_by_query(self,
                                   filter_=None,
                                   search_string=None,
                                   category=None,
                                   username=None,
                                   pages=None,
                                   per_page=None):
        scraper_data = OrderedDict({
        "title" : f"Nyaa Scraper v0.1 (Under construction v0204)",
        "description": f"Nyaa scraper for {search_string}"
        })
        search_url = self.create_search_query(filter_=filter_,
                                              search_string=search_string,
                                              category=category,
                                              username=username,
                                              search_type='scraper')
        print(f"Search link: '{search_url}")
        data = self.parse_scraper_data(url=search_url)
        return self.get_data(data)

        
debug = NyaaScraper()
pp = pprint.PrettyPrinter(indent=4)

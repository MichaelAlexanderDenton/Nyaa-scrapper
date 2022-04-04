"""
    TODO:
        ---if page returns empty, put an exception.
        ---category needs to be parse and converted.
        ---get files by their tier (trusted, success, not-trusted, neutral...)
        ---Add an exception if the page scrapped returned nothing
        ---Magnet links file can have more file info as optional
        ---"optional" add exceeding pages exception
"""
from bs4 import BeautifulSoup
from json import JSONDecodeError
from DataProcess import DataProcess
from collections import OrderedDict
import json
import pprint
class NyaaScraper(DataProcess):
    def __init__(self):
        super().__init__()
    
    ##################################################################
    ## Debug Methods for NyaaScraper
    ## You shouldn't be using these methods to get your data
    ##################################################################
    
    def _debug_show_titles(self):
        page_data = self.parse_scraper_data()
        mlist = list()
        for i in page_data['data']:
            mlist.append(i['title'])
        return mlist
    
    
    def get_latest_data(self, rtype='dict', pages=None, per_page=None):
        page_data = self._parse_scraper_data(pages=pages, per_page=per_page)
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
        pages_data = self._parse_scraper_data(pages=pages, per_page=per_page)
        self._get_data(pages_data)
        
    
    def get_latest_magnet_links(self, pages=None, per_page=None):
        pages_data = self._parse_scraper_data(pages=pages, per_page=per_page)
        self._get_magnet_links(pages_data)
        
        
    ##########################################################
    ## search_data_by_pages was removed due to be a spammy
    ## method to use
    ## Might add later.
    ##########################################################
    
    
    def get_data_by_query(self, filter_=None, search_query=None, category=None, username=None, pages=None, per_page=None):
        # Maybe we can move this somewhere else...
        scraper_data = OrderedDict({
            "title" : f"Nyaa Scraper v0.1 (Under construction v0204)",
            "description": f"Nyaa scraper for {search_query}"
        })
        search_url = self._create_search_query(
            filter_=filter_, 
            search_query=search_query, 
            category=category, 
            username=username,
            search_type="scraper")
        return self._parse_scraper_data(url=search_url, pages=pages, per_page=per_page)
    
    
    def get_torrent_files_by_query(self,
                                   filter_=None,
                                   search_query=None,
                                   category=None,
                                   username=None,
                                   pages=None,
                                   per_page=None):
        scraper_data = OrderedDict({
        "title" : f"Nyaa Scraper v0.1 (Under construction v0204)",
        "description": f"Nyaa scraper for {search_query}"
        })
        search_url = self._create_search_query(filter_=filter_,
                                              search_query=search_query,
                                              category=category,
                                              username=username,
                                              search_type='scraper')
        data = self._parse_scraper_data(url=search_url)
        return self._get_data(data)


    def get_magnet_links_by_query(self,
                                filter_=None,
                                search_query=None,
                                category=None,
                                username=None,
                                pages=None,
                                per_page=None):
        search_url = self._create_search_query(filter_=filter_,
                                              search_query=search_query,
                                              category=category,
                                              username=username,
                                              search_type='scraper')
        data = self._parse_scraper_data(url=search_url, pages=pages, per_page=per_page)
        return self._get_magnet_links(data)


    def get_data_by_username(self, username, rtype='dict', pages=None, per_page=None):
        search_url = self._create_search_query(username=username, search_type='scraper')
        data = self._parse_scraper_data(url=search_url, pages=pages, per_page=per_page)
        if rtype == 'dict':
            return data
        if rtype == 'json':
            return json.dumps(data)
        if rtype is not ["dict, json"]:
            raise TypeError("Specify data type for 'rtype' argument. 'dict' to return a dictionary, 'json' for JSON object notation.")

    def get_files_by_username(self, username:None, rtype='torrent', pages=None, per_page=None):
        search_url = self._create_search_query(username=username, search_type='scraper')
        data = self._parse_scraper_data(url=search_url, pages=pages, per_page=per_page)
        if rtype == 'magnet':
            return self._get_magnet_links(data)
        if rtype == 'torrent':
            return self._get_data(data)
        if rtype is not ['magnet', 'torrent']:
            raise TypeError("Please specify return type. either 'magnet' for links / 'torrent' for files ")
        
        
    def get_torrent_by_id(self, id_=None):
        self._get_file(id_=id_)
    
    
    def get_magnet_by_id(self, id_=None, file=None):
        return self._get_magnet(id_=id_, file=file)


scraper = NyaaScraper()
scraper.get_latest_torrent_files(pages=1, per_page=10)
import requests
import re
import os
from collections import OrderedDict
from bs4 import BeautifulSoup
class DataProcess(object):
    def get_torrent_link(self, url):
        BASE_TORRENT_LINK = "https://nyaa.si/download/"
        torrent_id = re.findall(r'([0-9]+)', url)[0]
        return '{0}{1}.torrent'.format(BASE_TORRENT_LINK, torrent_id)
    
    def get_magnet_link(self, url):
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'lxml')
        return soup.find('a', 'card-footer-item').get('href').strip()
    
    def parse_rss_feed(self, url, limit=None):
        """"Parse the RSS feed coming from Nyaa.si website
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        Basic usage:
            self.parse_rss_feed('http://nyaa.si/?page=rss&more_query_chain_here', 'json')
        Args:
            url (str): URL to the desired RSS feed
            type (str, optional): Data structure returned from the function:
                dict -> Returns a dictionnary with key/value pairs
                json -> Returns a JSON notation
                Default value -> JSON notation.
        """
        html = requests.get(url).content
        soup = BeautifulSoup(html, features='lxml')
        # saving data as an ordered list
        obj = OrderedDict({
            "title" : 'Nyaa - Home - Torrent File Feed Parser',
            "description": 'Feed Parser for Home',
            "atom": {
                'link': soup.find('atom:link').get('href'),
                'rel': soup.find('atom:link').get('rel'),
                'type': soup.find('atom:link').get('type'),
            },
            "data": list(),    
        })

        # Find all torrent files and magnets
        items = soup.find_all('item')
        for item in (items[:limit] if limit is not None else items):
            anime = OrderedDict()
            anime['title'] = item.title.text.strip()
            anime['torrent_file'] = self.get_torrent_link(item.guid.text.strip())
            anime['info_link'] = {
                "url" : item.guid.text.strip(),
                "isPermaLink" : item.guid.get('isPermaLink')
            }
            anime['Published_at'] = item.pubdate.text.strip()
            anime['seeders'] = item.find('nyaa:seeders').text.strip()
            anime['leechers'] = item.find('nyaa:leechers').text.strip()
            anime['downloads'] = item.find('nyaa:downloads').text.strip()
            anime['infoHash'] = item.find('nyaa:infohash').text.strip()
            anime['category'] ={
                'id' : item.find('nyaa:categoryid').text.strip(),
                'category__name' : item.find('nyaa:category').text.strip()
            },
            anime['file__size'] = item.find('nyaa:size').text.strip()
            anime['comments'] = item.find('nyaa:comments').text.strip()
            anime['is__trusted__torrent'] = {
                'text' : item.find('nyaa:trusted').text.strip(),
                'value': False if item.find('nyaa:trusted').text.strip() == 'No' else True, 
            },
            anime['is__remake'] = item.find('nyaa:remake').text.strip()
            obj['data'].append(anime)
        return obj


    # Quality query is missing
    def RSS_create_search_query(self, filter_=None, search_string=None, category=None, username=None):
        base_url = 'https://nyaa.si/?page=rss'
        query_array = list()
        query = str()
        rss_queries = ['filter', 'q', 'c', 'u']
        if filter_ is not None:
            query_array.append(dict({"f" : filter_}))
        if search_string is not None:
            search_string = search_string.replace(' ', '+')
            query_array.append(dict({"q": search_string}))
        if category is not None:
            query_array.append(dict({"c" : category}))
        if username is not None:
            query_array.append(dict({"u" : username}))
        
        for q in query_array:
            for key, value in q.items():
                query += f"&{key}={value}"
        return (base_url + query)
    
    
    def get_torrent_files(self, url, limit=None):
        feed_data = self.parse_rss_feed(url, limit=limit)
        base_dir = os.path.dirname(__file__)
        mdir = os.path.join(base_dir, "automated")
        if os.path.exists(mdir) == False:
            os.mkdir(mdir)
            print('Directory created.')
        else:
            print('directory exists.')
        for item in feed_data['data']:
            with requests.get(item['torrent_file'], stream=True) as r:
                r.raise_for_status()
                invalid_chars = f'<>:"\/|?*'
                pattern = r'[' + invalid_chars + ']'
                new_name = re.sub(pattern, ' ', item['title'])
                with open(os.path.join(mdir, 'log.txt'), 'a', encoding='utf-8') as log:
                    log.write(f"File saved: {new_name}.torrent \n")
                with open(os.path.join(mdir, f"{new_name}.torrent"), "wb") as f:
                    for chunk in r.iter_content():
                        if chunk:
                            f.write(chunk)  
                        




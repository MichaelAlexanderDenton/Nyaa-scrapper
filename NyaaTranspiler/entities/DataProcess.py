import requests
import re
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
        magnet = soup.find('a', 'card-footer-item').get('href').strip()
        return magnet
    
    def parse_rss_feed(self):
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
        html = requests.get('https://nyaa.si/?page=rss').content
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
        count = 0
        for item in items:
            if count == 10:
                break
            else:
                count = count + 1
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


debug = DataProcess()
debug.parse_rss_feed()

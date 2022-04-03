"""
    ----Creating the automated directory needs its own function called by __init__
    ----requests.exceptions.HTTPError: 404 Client Error: NOT FOUND for url: https://nyaa.si/download/647951
"""

import requests
import urllib.parse
import urllib3
import re
import os
import pprint
from collections import OrderedDict
from bs4 import BeautifulSoup
class DataProcess(object):
    def __init__(self):
        self.base__url = "http://nyaa.si/?"
        self.base__rss_url = "https://nyaa.si/?page=rss"
        self.base__torrent__link = "https://nyaa.si/download/"
        self.base__view__link = "https://nyaa.si/view/"
        self.base__dir = os.path.dirname(__file__)
        
    def _check_registration(self):
        html = requests.get('https://nyaa.si/register').content
        soup = BeautifulSoup(html, 'lxml')
        if soup.find('pre'):
            return "Registations are currently closed."
        else:
            return "Registrations are now open."
        
    def get_torrent_link(self, url):
        BASE_TORRENT_LINK = "https://nyaa.si/download/"
        torrent_id = re.findall(r'([0-9]+)', url)[0]
        return '{0}{1}.torrent'.format(BASE_TORRENT_LINK, torrent_id)
    
    
    def create_torrent_link_by_id(self, id=int()):
        return '{0}{1}.torrent'.format(self.base__torrent__link, id)
    
        
    def get_magnet_link(self, url):
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'lxml')
        return soup.find('a', 'card-footer-item').get('href').strip()
    
    def _parse_rss_feed(self, url=None, limit=None):
        _count = 0
        url = self.base__rss_url if url is None else url
        html = requests.get(url).content
        soup = BeautifulSoup(html, features='lxml')
        # saving data as an ordered list
        obj = OrderedDict({
            "title" : 'Nyaa - Home - Torrent File Feed Parser',
            "description": f'Feed Parser for Home',
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
            _count += 1
            obj['data'].append(anime)
        print(f"Total of {_count} object(s) were created from the RSS feed.")
        return obj


    def _create_search_query(self, filter_=None, search_query=None, category=None, username=None, search_type=None):
        base_url = self.base__rss_url if search_type == 'rss' else self.base__url
        query_array = list()
        query = str()
        if filter_ is not None:
            query_array.append(dict({"f" : filter_}))
        if search_query is not None:
            search_query = search_query.replace(' ', '+')
            query_array.append(dict({"q": search_query}))
        if category is not None:
            query_array.append(dict({"c" : category}))
        if username is not None:
            query_array.append(dict({"u" : username}))
        
        for q in query_array:
            for key, value in q.items():
                query += f"&{key}={value}"
                
        link = base_url + query  
        print(f"Search link: {link}")
        return link
    
    # RSS torrent file retrieval
    def _rss_get_torrent_files(self, url=None, limit=None):
        feed_data = self._parse_rss_feed(url=url, limit=limit)
        return self.get_data(feed_data)


    def _get_file(self, id_):
        try:
            # get file name first
            html = requests.get((self.base__view__link + str(id_))).content
            soup = BeautifulSoup(html, 'lxml')
            title = soup.find('h3', 'panel-title').text.strip()
            url = f"{self.base__torrent__link}{id_}.torrent"
            mdir = os.path.join(self.base__dir, "automated")
            if os.path.exists(mdir) == False:
                os.mkdir(mdir)
                print('Directory created.')
            else:
                print('directory exists.')
            print(f"file name: {title}")
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                invalid_chars = f'<>:"\/|?*'
                pattern = r'[' + invalid_chars + ']'
                new_name = re.sub(pattern, ' ', title)[:155]                # As Windows files are 155 character-limited.
                with open(os.path.join(mdir, 'log.txt'), 'a', encoding='utf-8') as log:
                    log.write(f"File saved: {new_name}.torrent \n")
                    with open(os.path.join(mdir, f"{new_name}.torrent"), "wb") as f:
                        for chunk in r.iter_content():
                            if chunk:
                                f.write(chunk)      
        finally:
            print('file saved.')

    # get multiple files from structure                  
    def _get_data(self, item_list):
        """
            Download torrent files from a list of item provided by _parse_rss_feed()
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        args:
            item_list   --> a list of items with item'[torrent_link'] attr to retrieve torrent link
            
        """
        try:
            _count = 0
            mdir = os.path.join(self.base__dir, "automated")
            # check if directory exists
            if os.path.exists(mdir) == False:
                os.mkdir(mdir)
                print('Directory created.')
            else:
                print('directory exists.')
                
            for item in item_list['data']:
                with requests.get(item['torrent_file'], stream=True) as r:
                    r.raise_for_status()
                    invalid_chars = f'<>:"\/|?*'
                    pattern = r'[' + invalid_chars + ']'
                    new_name = re.sub(pattern, ' ', item['title'])[:155]        # As Windows files are 155 character-limited.
                    with open(os.path.join(mdir, 'log.txt'), 'a', encoding='utf-8') as log:
                        log.write(f"File saved: {new_name}.torrent \n")
                        with open(os.path.join(mdir, f"{new_name}.torrent"), "wb") as f:
                            for chunk in r.iter_content():
                                if chunk:
                                    f.write(chunk)
                    _count += 1
        finally:
            print(f"Downloaded {_count} torrent files.")
            
    def _get_magnet(self, id_, file=False):
        view_link = "{0}{1}".format(self.base__view__link, str(id_))
        html = requests.get(view_link).content
        soup = BeautifulSoup(html, 'lxml')
        if file == True:
            with open(os.path.join((self.base__dir + r'\automated'), 'magnet.txt'), "w") as f:
                f.write(soup.find('a', 'card-footer-item').get('href'))
                f.close()
                return
        if file == False:
            return print(soup.find('a', 'card-footer-item').get('href'))
                        

    # This is purely exprimental, not guaranteed to 
    # work properly long-term due to trackers changing their
    # udp/port, but we'll see...
    
    def create_magnet_link(self, infohash=str(), title=str()):
        magnet_prefix = "magnet:?xt=urn:"
        torrent_infohash = f"btih:{infohash}"
        torrent_title = f"&dn={title}"
        
        # Gathering trackers from torrents in the main page and the upload page
        
        html = requests.get("https://nyaa.si/").content
        soup = BeautifulSoup(html, 'lxml')
        magnets = soup.find_all('i', "fa-magnet")
        for m in magnets[:3]:
            x = m.parent['href']
            x = urllib.parse.unquote(x)
            # print(f"{x}\n")
            test = re.findall(r"&tr=(.+)announce", x)[0]
            test = test.split("&")
            
        # Constructing links
        # ---- Under construction ----
            magnet = f"{magnet_prefix}{torrent_infohash}{urllib.parse.quote(torrent_title)}"
        for m in test:
            magnet += f"&{urllib.parse.quote(m)}"

        return magnet
            
            
    ########################################################
    # Nyaa Scraper methods/properties
    ########################################################
    
    def _parse_scraper_data(self, url="http://nyaa.si/", pages=None, per_page=None):
        _count = 0
        if pages == None:
            print("Pages value was not provided.")
            print("Scraping only the first page.")
        else:  
            print(f"----Number of pages to scrape > {pages}")
        data = OrderedDict({'data': list()})
        try:
            for p in range(1, (2 if pages is None else (pages + 1))):
                if pages is not None:
                    # kind of a hack, but it works
                    if url[-1] == "/":
                        url = url + "?"
                    create_url = url + f"&p={p}"
                    print(create_url)
                html = requests.get(create_url if pages is not None else url).content
                soup = BeautifulSoup(html, "lxml")
                items_list = soup.find('tbody').find_all('tr')
                for i in items_list[0:per_page] if per_page is not None else items_list:
                    anime = OrderedDict()
                    anime_category = i.select('td:nth-of-type(1)')          # Done
                    anime_name_info = i.select('td:nth-of-type(2)')         # Done
                    anime_torrent_magnet = i.select('td:nth-of-type(3)')    # Done
                    data_size = i.select('td:nth-of-type(4)')               # Done
                    anime_timestamp = i.select('td:nth-of-type(5)')         # Done
                    anime_seeders = i.select('td:nth-of-type(6)')           # Done
                    anime_leechers = i.select('td:nth-of-type(7)')          # Done
                    number_of_downloads = i.select('td:nth-of-type(8)')     # Done
                    
                    
                    # Scrape title/hyperlink
                    for info in anime_name_info:
                        link = self.base__url + info.find('a')['href']
                        if info.find("a", 'comments'):
                            anime['title'] = info.find('a').findNext('a').get('title')
                            anime['link'] = link.split("#")[0].strip()
                            anime['comments'] = int(info.find('a', 'comments').get('title').split(' ')[0])
                        else:
                            anime['title'] = info.find('a').get('title')
                            anime['link'] = link
                            anime['comments'] = 0
                    
                    # Scrape category
                    for find_category in anime_category:
                        anime['category'] = OrderedDict({
                            'category__name' : find_category.find('img')['alt'],
                            'category__tag' : find_category.find('a')['href'].split('=')[1]
                        })
                        
                    # Scrape torrent/magnet links
                    for link in anime_torrent_magnet:
                        torrent__link = self.base__url + link.find('i', 'fa-download').parent['href']
                        magnet__link = link.find('i', 'fa-magnet').parent['href']
                        anime['torrent_file'] = torrent__link
                        anime['magnet_link'] = magnet__link
                    
                    # Scrape filesize
                    anime['size'] = data_size[0].text 
                    
                    # Scrape timestamp
                    time = OrderedDict({
                        "created_at" : anime_timestamp[0].text,
                        "timestamp": anime_timestamp[0].get('data-timestamp'),
                        # "real_time": anime_timestamp[0].get('title')              #JS-executed
                    })        
                    anime['date'] = time
                    # Seeders/Leechers
                    seeders = anime_seeders[0].text
                    leechers = anime_leechers[0].text
                    anime['seeders'] = seeders
                    anime['leechers'] = leechers          
                    
                    # Downloads
                    dnwlds = number_of_downloads[0].text
                    anime['downloads'] = dnwlds
                    _count += 1
                    data['data'].append(anime)
                if pages is not None:
                    print(f"End of page {p}")
            print(f"Total data scraped: {_count} in {pages} pages.") if pages is not None else print(f'Total data scraped: {_count} in one page.')
            return data
        except (urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError, requests.exceptions.ConnectionError ) as e:
            print('no connection error')


    def _get_magnet_links(self, item_list):
        try:
            _count = 0
            mdir = os.path.join(self.base__dir, "automated")
            if os.path.exists(mdir) == False:
                os.mkdir(mdir)
                print('Directory created.')
            else:
                print('directory exists.')
            with open(os.path.join(mdir, 'magnets.txt'), "w") as f:
                for i in item_list['data']:
                    f.write(f"{i['magnet_link']} \n")
                    _count += 1
            f.close()
        finally:
            print(f"Saved {_count} magnet links.")


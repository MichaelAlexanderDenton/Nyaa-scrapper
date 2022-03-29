from DataProcess import DataProcess
import json
import requests
import os
import re
from json import JSONDecodeError
import pprint
import string
class NyaaRSS(DataProcess):
    def RSS_get_feed_data(self, rtype=None):
        feed_data = self.parse_rss_feed()
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
        
    def RSS_get_torrent_files(self):
        feed_data = self.RSS_get_feed_data(rtype='dict')
        for item in feed_data['data']:  
            with requests.get(item['torrent_file'], stream=True) as r:
                base_dir = os.path.dirname(__file__)
                mdir = os.path.join(base_dir, "automated")
                r.raise_for_status()
                test = f'<>:"\/|?*'
                pattern = r'[' + test + ']'
                new_name = re.sub(pattern, ' ', item['title'])
                with open(os.path.join(mdir, f"{new_name}.torrent"), "wb") as f:
                    for chunk in r.iter_content():
                        if chunk:
                            f.write(chunk)
            # with requests.get(item['torrent_file,'] , stream=True) as r:
            #     r.raise_for_status()
            #     with open(f"automated/{item['title']}.torrent", 'wb') as f:
            #         for chunk in r.iter_content(chunk_size=512):
            #             if chunk:
            #                 f.write(chunk)
                
            
rss = NyaaRSS()
rss.RSS_get_torrent_files()

base_dir = os.path.dirname(__file__)
mdir = os.path.join(base_dir, "automated")
print(mdir)
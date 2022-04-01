from bs4 import BeautifulSoup
from DataProcess import DataProcess
class NyaaScraper(DataProcess):
    def __init__(self):
        self.base__url = "http://nyaa.si/"
    
    
    def get_latest_torrent_data(self, rtype=None):
        page_data = self.parse_scraper_data(pages=1)
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
    
    
    def get_latest_torrent_files(self):
        pages_data = self.parse_scraper_data(pages=1)
        self.get_data(pages_data)
        
        
debug = NyaaScraper()
debug.get_latest_torrent_files()
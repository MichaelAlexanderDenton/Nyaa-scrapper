from DataProcess import DataProcess
class NyaaRSS(DataProcess):
    def __init__(self):
        self.BaseUrl = 'https://nyaa.si/?page=rss'
        
    
    def RSSGetLatestMagnetLinks(self):
        lst = self.parse_rss_feed(self.BaseUrl, rtype="dict")
        for item in lst.data:
            pass



rss = NyaaRSS()
print(rss.RSSGetLatestMagnetLinks())
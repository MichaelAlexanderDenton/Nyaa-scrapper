from DataProcess import DataProcess
import json
from json import JSONDecodeError
import pprint

class NyaaRSS(DataProcess):
    def RSS_get_feed_data(self, rtype=None):
        feed_data = self.parse_rss_feed()
        try:
            if rtype == 'json':
                return json.dumps(obj)
            if rtype == 'dict':
                return obj
            if rtype == 'debug':
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(rtype(obj))
            if rtype is not ['json', 'dict', 'debug']:
                raise TypeError('Invalid type, try again. i.e --> type="dict"/type="json"')
        except JSONDecodeError:
            raise ('Invalid type, try again. i.e --> rtype="dict"/rtype="json"')
# -*- coding: utf-8 -*-

"""
NyaaScraper

NyaaScraper is Feed parser and a web scraper for Nyaa.si and sukebei.nyaa.

NyaaScraper modules:
        DataProcess.py --> contains DataProcess class. has all the necessary methods for extracting data from both RSS and the website
        NyaaRSS.py     --> contains NyaaRSS class. all methods needed to get data from the RSS feed.
        NyaaScraper.py --> contains NyaaScraper class. all methods needed to get data from the website using Beautifulsoup.
"""


__version__ = "1.0.0"
__license__ = "MIT"
__source_url__ = "https://github.com/MichaelAlexanderDenton/nyaa-scrapper"
__author__ = "Mike Denton"

# imports
from .DataProcess import DataProcess
from .NyaaRSS import NyaaRSS
from .NyaaScraper import NyaaScraper
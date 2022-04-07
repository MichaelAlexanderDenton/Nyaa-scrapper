# NyaaPy Downloader
A simple, yet useful Nyaa.si web scraper and RSS feed parser.

NyaaPy is a RSS feed parser and web scraper for Nyaa.si website, you can search for metadata using ID, username...etc
and get data in a dict form or JSON for your own use.

## Get Started.

To get started. instantiate NyaaRSS or NyaaScraper class depending on your need, you can set the main directory or leave it empty. Default directory would be : './automated'

```

    # instantiating RSS class
    rss = NyaaRSS(directory="your/custom/directory/")

    # instantiating scraper class
    scraper = NyaaScraper()

    # Get latest RSS feed data as a dictionary
    rss.get_latest_feed_data()

    # Or you can get torrent files for your search input!
    scraper.get_torrents_by_query(search_query="Digimon Adventure", category=("Anime", "English-translated"))

```

## NyaaRSS

NyaaRSS is a feed parser for the RSS feed from nyaa.si, it takes the data that comes from the feed and parse it into a dict or
a JSON notation in a more readable way, with more metainfo in it, or you can save this info somewhere in a file or download 
all torrent files that are available in that feed.

### self.get_latest_feed_data(rtype=str(), limit=int())

Get and parser metadata from the RSS feed, you'll need to pass the return type (rtype), it can be either a 'dict' for dictionary, or 'json' for JSON, no value will resolve to 'dict'. otherwise, it'll raise a ValueError. limit will limit how
many items it gets from the feed, should be a number int() or a str() as a number. If the value is not entered, it'll scrape
the entire page

rss.get_latest_feed_data(rtype='json', limit=5)

### self.get_latest_torrent_files(limit=int())


You can download the torrent files available in the feed with just one simple function! It takes one parameter, limit, which is
the same from [get_latest_feed_data()]. if default directory wasn't changed, it'll be './automated'

rss.get_latest_torrent_files()

### self.get_data_by_query(filter_=None, search_query=None, category=None, username=None, limit=None)


This method will get and parse data using a custom search, it takes severals parameters to refine your search:
filter_ ==>
search_query ==> Your search text.
category ==>
username ==> torrents posted by this user
limit ==> limit how many items you get from the feed.

rss.get_data_by_query(filter_='no remake', search_query='Digimon Adventure', category=('anime', "English Translated"), username="TonyGabagoolSoprano")


### self.get_torrents_by_query(filter_=None, search_query=None, category=None, username=None, limit=None)
Works the same as get_data_by_query(), but instead, it'll download all torrent files in the RSS feed.

rss.get_torrents_by_query(filter_='no remake', search_query='Digimon Adventure', category=('anime', "English Translated"), username="TonyGabagoolSoprano")


### Getting data by username
While you can do this with the methods above, this just facilitate the search by username with a small function.

### get_data_by_username(username=str())
Gets data from the feed by username, takes one parameter, an str(). returns data as dict('json' has not been implemented yet.)
self.get_data_by_username(username="GetMeSomeGabagool69")

Or you can use get_torrents_by_username() to download all torrent files from that feed.


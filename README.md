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
a JSON notation. with more metainfo in it, or you can save this info somewhere in a file or download  all torrent files that are available in the feed.

### Get latest feed data

``` self.get_latest_feed_data(rtype=str(), limit=int()) ```

Get and parse metadata from the RSS feed, you'll need to pass the return type (rtype), it can be either a 'dict' for dictionary, or 'json' for JSON, no value will resolve to 'dict'. otherwise, it'll raise a ValueError. limit will limit how many items it gets from the feed, should be a number int() or a str() as a number. If the value is not entered, it'll scrape the entire page.

``` rss.get_latest_feed_data(rtype='json', limit=5) ```

### Get Latest Torrent files from the feed:

``` self.get_latest_torrent_files(limit=int()) ```

You can download the torrent files available in the feed with just one simple function! It takes one parameter, limit, which is
the same from [get_latest_feed_data()]. if default directory wasn't changed, all files downloaded are gonna be stored in: './automated'.
```
# limit is optional.
rss.get_latest_torrent_files(limit=5)
```

### Get Search metadata from the feed:

``` self.get_data_by_query(filter_=None, search_query=None, category=None, username=None, limit=None) ```

This method will get and parse data using a custom search, it takes severals parameters to refine your search: <br />

filter_ ==> str. Can be either "no filter", "no remake", "trusted only", if no value was entered, it won't be passed on the query. raises ValueError if the value wasn't not in any of the filters above.<br />

search_query ==> str. Your search text, raises ValueError if this parameter was not passed.<br />

category ==> tuple. category must be (your_main_category, your_sub_category). won't be included in query if nothing was passed.<br />

username ==> str. Torrents posted by that user.<br />

limit ==> int. Limit how many items you get from the feed.<br />

``` rss.get_data_by_query(filter_='no remake', search_query='Digimon Adventure', category=('anime', "English-translated"), username="TonyGabagoolSoprano")```

You can also download all torrent files using:

``` self.get_torrents_by_query(filter_="trusted only", search_query='Digimon Adventure', category=('anime', "English Translated"), limit=20) ```

Works the same as get_data_by_query(), but instead, it'll download all torrent files in the RSS feed.


### Getting data by username

While you can do this with the methods above, this just facilitate the search by username with a small function.

``` self.get_data_by_username(username="GetMeSomeGabagool69") ```

Or you can use get_torrents_by_username() to download all torrent files from that feed:

``` self.get_torrents_by_username(username="GetMeSomeGabagool69") ```

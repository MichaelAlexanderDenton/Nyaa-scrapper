[08/04/2022] : First public release. <br />
[29/03/2022] : Initial Commit.

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

```filter_``` ==> str. Can be either "no filter", "no remake", "trusted only", if no value was entered, it won't be passed on the query. raises ValueError if the value wasn't not in any of the filters above.<br />

```search_query``` ==> str. Your search text, raises ValueError if this parameter was not passed.<br />

```category``` ==> tuple. category must be (your_main_category, your_sub_category). won't be included in query if nothing was passed.<br />

```username``` ==> str. Torrents posted by that user.<br />

```limit``` ==> int. Limit how many items you get from the feed.<br />

``` rss.get_data_by_query(filter_='no remake', search_query='Digimon Adventure', category=('anime', "English-translated"), username="TonyGabagoolSoprano")```

You can also download all torrent files using:

``` self.get_torrents_by_query(filter_="trusted only", search_query='Digimon Adventure', category=('anime', "English Translated"), limit=20) ```

Works the same as get_data_by_query(), but instead, it'll download all torrent files in the RSS feed.


### Getting data by username

While you can do this with the methods above, this just facilitate the search by username with a small function.

``` self.get_data_by_username(username="GetMeSomeGabagool69") ```

Or you can use get_torrents_by_username() to download all torrent files from that feed:

``` self.get_torrents_by_username(username="GetMeSomeGabagool69") ```


# NyaaScraper

NyaaScraper is a web scraper version of NyaaRSS, with a few additional methods that makes your search a lot easier! To instantiate a class, you simply:

```
    # Instantiate a class
    # Directory parameter is optional.
    scraper = NyaaScraper(directory="C:/downloads")         # Make sure that directory exists!

```

## Scrape latest data:

This works the same as rss.get_latest_feed_data(), with the advantage of going through multiple pages and scrape data off of them:

``` 
    # getting data from the first two pages
    scraper.get_latest_data(rtype="json", pages=2, per_page=10)
```
This will fetch data from the first two pages, and get 10 items from each page and returns the results as a JSON object.

There's also another method that downloads torrent files off these pages!:

``` 
    # getting torrent files from the first two pages
    scraper.get_latest_torrent_files(pages=2, per_page=10)
```

Or, if you want to get magnet links only, there's also a method for that!:

``` 
    # getting torrent files from the first two pages
    scraper.get_latest_magnet_links(pages=2, per_page=10)
```

## Scrape data by search input:

You can make a custom search input and extract data/torrents/magnets off of it. It takes the same parameters as rss.get_data_by_query():

``` 
    # Get data by using a search_query
    scraper.get_data_by_query(filter_="no remake", search_query="Digimon Adventure", category=("Anime", "Raw"), pages=2)
    
    # Get torrent files
    scraper.get_torrent_files_by_query(search_query="Digimon Adventure", pages=3, per_page=15)
    
    # Get magnet links
    scraper.get_magnet_links_by_query(category=("Literature", "Raw"), search_query="Digimon Adventure", pages=3, per_page=15)       # It's fu#king RAW!!!
    
```
The only additional parameters for these methods are: <br />
``` pages ```       ==> takes a number. if no value was present, it'll only scrape the first page. Optional.
``` per_page ```    ==> takes a number. if no value was present, it'll scraper all items available in the pages. Optional.

# Scrape data by username:

Takes a username as a parameter, raises an error if no value was present:
```
   # receiving data by username as a dictionary
   scraper.get_data_by_username(username="TonyGabagoolSoprano69", rtype="dict", pages=4, per_page=23) 
   
```

One method that is different from the ones above is get_files_by_username(). It takes a new parameter ```rtype```, "magnet" for saving magnet links a ```.txt``` format, or "torrent" for downloading torrent files:

```
    # downloading torrent files by username
    scraper.get_files_by_username(rtype="torrent", username="TonyGabagoolSoprano69")
    
    # saving magnet links:
    scraper.get_files_by_username(rtype="magnet", username="TonyGabagoolSoprano69")
    
```
Raises an ValueError if no ```rtype``` was present.


## Downloading single file by ID:
This can be handy in some situations, all you need is an ID and the method will fetch that file/magnet link for you!

```
    scraper.get_torrent_by_id(id_=1440531)
```

```id_```       ==> takes a number, returns a ValueError if no ```id_``` was entered.

Or magnet links:

```
    scraper.get_magnet_by_id(id_=1440531, file=True)
```

``` file ```    ==> Boolean. default set to ``` False ``` and will return the magnet link, ``` True ``` will save the magnet in the directory (default ``` ./automated ```) as ``` magnet.txt ```

``` 
    This document, and the program are still under development, if any bugs or mistakes on the document, either pull a request and fix it if you know how,
    or just report it to the issues section and I'll get to it.
    
    This is my first program I wrote, so it's not very pretty, any suggestions or any website to scrape or ideas, let me know ;-)
  
```


"""
Program:        crawler.py
Author:         Bill Jameson (jamesw2@rpi.edu)
Description:    Provides functions to:
                    - crawl a URL and collect stats about links and word occurrences
                    - crawl a site and collect stats about links and word occurrences
                    - analyze & format the stats collected by the site crawler
"""

import urllib.request
import urllib.error

def crawlURL(URL):
    """Retrieve the web page at URL and parse it for links and words.
       Return 3 values:
       - the number of bytes retrieved (-1 if an error is encountered)
       - a list of tuples containing the links harvested and their corresponding link text
       - a dictionary containing all the unique words encountered and their word counts"""
    req = urllib.request.Request(URL)
    try:
        resp = urllib.request.urlopen(req)
    except URLError as e:
        # Return early if there's an error (including the page requiring authentication).
        return -1, [], {}
    else:
        print(resp)

def crawlSite(rootURL):
    print("")

def analyzeStats(bytes, URLs, words):
    print("")

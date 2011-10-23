"""
Program:        crawler.py
Author:         Bill Jameson (jamesw2@rpi.edu)
Description:    Provides functions to:
                    - crawl a URL and collect stats about links and word occurrences
                    - crawl a site and collect stats about links and word occurrences
                    - analyze & format the stats collected by the site crawler
"""
import re
from urllib.request import Request, urlopen
from urllib.error import URLError

def parsePage(resp):
    """Parse the page that response resp provides a connection to.
       Arguments: resp is an object of type http.client.HTTPResponse
       Returns 3 values:
       - the size of the page (in bytes)
       - a list of tuples describing the page's links; each tuple is (address, link text)
       - a dictionary mapping all the words that occur outside of HTML tags to their counts"""
    mimeType = resp.getheader('Content-Type')
    if not mimeType.startswith('text'):
        # Can't easily parse non-text for links/words, so just return the file size.
        # If the HTTP request header includes the Content-Length, use that since read()
        #   can take a long time for media files.
        if resp.getheader('Content-Length') is not None:
            return int(resp.getheader('Content-Length')), [], {}
        else:
            return len(resp.read()), [], {}
    else:
        # Parse words and links from text documents, while ignoring tags.
        # Tag-ignoring logic will ignore everything within angle brackets, even in plaintext.
        contents = resp.read().decode('utf-8')
        # NB: this pattern does not match links with a missing </a> tag.
        linkPattern = '<a .*?href="(.*?)".*?>(.*?)</a>'
        links = re.finall(linkPattern, contents)

def crawlURL(URL):
    """Retrieve the web page at URL and parse it for links and words.
       Return 3 values:
       - the number of bytes retrieved (-1 if an error is encountered)
       - a list of tuples containing the links harvested and their corresponding link text
       - a dictionary containing all the unique words encountered and their word counts"""
    req = urllib.request.Request(URL)
    try:
        resp = urllib.request.urlopen(req)
        bytes, links, words = parsePage(resp)
        return bytes, links, words
    except URLError as e:
        # Return early if there's an error (including the page requiring authentication).
        return -1, [], {}

def crawlSite(rootURL):
    # List of whistelisted MIME types to recursively crawl (only parse text-based ones)
    mimeTypes = ['text/html']

def analyzeStats(bytes, URLs, words):
    print("")

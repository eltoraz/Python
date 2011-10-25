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

def expandURL(URL, topLevel):
    """Expand URL if it's not an absolute path, using topLevel as the prefix.
       Returns a string containing the expanded URL."""
    if re.match('http://|ftp://|www\.', URL) != None:
        return URL
    else:
        r1 = topLevel
        r2 = URL
        if topLevel.endswith('/'):
            r1 = topLevel[:len(topLevel)-1]

        if URL.startswith('/'):
            r2 = URL[1:]
        
        return topLevel + '/' + URL

def parsePage(resp):
    """Parse the page that response resp provides a connection to.
       Arguments: resp is an object of type http.client.HTTPResponse
       Returns 3 values:
       - the size of the page (in bytes)
       - a list of tuples describing the page's links; each tuple is (address, link text)
       - a dictionary mapping all the words that occur outside of HTML tags to their counts"""
    # Parse words and links from text documents, while ignoring tags.
    # Tag-ignoring logic will ignore everything within angle brackets, even in plaintext.
    contents = resp.read()
    bytes = len(contents)
    contents = contents.decode('utf-8')

    # Remove everything in a comment.
    contents = re.sub('<!--.*?-->', '', contents, 0, re.S)

    # Remove all non-link text.
    contents = re.sub('(?!</a>)<(?!a ).*?>', '', contents, 0)

    # Parse out the links and link text, then remove link tags.
    # NB: this pattern does not match links with a missing </a> tag.
    linkPattern = '<a .*?href="(.*?)".*?>(.*?)</a>'
    rawLinks = re.findall(linkPattern, contents, re.I)
    links = []
    topLevelURL = resp.geturl()
    for l in rawLinks:
        fullURL = expandURL(l[0])
        if fullURL.startswith(topLevelURL):
            links.append((fullURL, topLevelURL, l[1]))
    contents = re.sub('<.*?>', '', contents, 0)

    words = {}

    return bytes, links, words

def crawlURL(URL):
    """Retrieve the web page at URL and parse it for links and words.
       Return 3 values:
       - the number of bytes retrieved (-1 if an error is encountered)
       - a list of tuples containing the links harvested and their corresponding link text
       - a dictionary containing all the unique words encountered and their word counts"""
    req = Request(URL)
    try:
        resp = urlopen(req)
    except URLError as e:
        # Return early if there's an error (including the page requiring authentication).
        return -1, [], {}
    
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
        bytes, links, words = parsePage(resp)
        return bytes, links, words

def crawlSite(rootURL):
    # List of whistelisted MIME types to recursively crawl (only parse text-based ones)
    mimeTypes = ['text/html']

def analyzeStats(bytes, URLs, words):
    print("")

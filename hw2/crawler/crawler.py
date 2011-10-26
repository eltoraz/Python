"""
Program:        crawler.py
Author:         Bill Jameson (jamesw2@rpi.edu)
Description:    Provides functions to:
                    - crawl a URL and collect stats about links and word occurrences
                    - crawl a site and collect stats about links and word occurrences
                    - analyze & format the stats collected by the site crawler
"""
import re
from time import sleep
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
        
        return r1 + '/' + r2

def countWords(text):
    """Return a dictionary of unique words to their counts in the supplied text.
       For best results, strip the text of HTML tags (etc.) beforehand."""
    words = {}

    # Split the text on any non-word characters.
    # Count numbers as words and allow apostrophes in possessives.
    split = re.split('(?!\'s)\W+', text)

    # Populate the dictionary.
    for w in split:
        lc = w.lower()
        if lc == '':    # The split sometimes inserts empty strings at the start/end.
            pass
        elif lc in words:
            words[lc] += 1
        else:
            words[lc] = 1
    
    return words

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

    # Remove everything in a comment and scripts.
    contents = re.sub('<!--.*?-->|<script.*?</script>', '', contents, 0, re.S)

    # Remove all non-link text.
    contents = re.sub('(?!</a>)<(?!a ).*?>', '', contents)

    # Parse out the links and link text, then remove link tags.
    # The only links returned are those in the same domain, and the text is '' for images.
    # NB: this pattern does not match links with a missing </a> tag.
    linkPattern = '<a .*?href="(.*?)".*?>(.*?)</a>'
    rawLinks = re.findall(linkPattern, contents, re.I)
    links = []
    topLevelURL = resp.geturl()
    for l in rawLinks:
        fullURL = expandURL(l[0], topLevelURL)
        if fullURL.startswith(topLevelURL):
            links.append((fullURL, l[1]))
    contents = re.sub('<.*?>', '', contents)

    words = countWords(contents)

    return bytes, links, words

def crawlURL(URL):
    """Retrieve the web page at URL and parse it for links and words.
       Return 3 values:
       - the number of bytes retrieved (-1 if an error is encountered)
       - a list of tuples containing the links harvested and their corresponding link text
       - a dictionary containing all the unique words encountered and their word counts
       On error, return -1, [], {}."""
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
    """Crawl an entire website from rootURL, parsing out links and words.
       Return 3 values:
       - the number of bytes retrieved (-1 if an error is encountered)
       - a list of tuples containing the links harvested and their corresponding link text
       - a dictionary containing all the unique words encountered and their word counts
       On rootURL error, return -1, [], {}.
       Ignore subpage errors."""
    # Politeness policy: sleep for 3 seconds between connections.
    sleepTime = 3
    crawledLinks = []

    bytes = 0
    links = []
    words = {}

    # Crawl the root URL to get the initial set of links to work off of
    newBytes, newLinks, newWords = crawlURL(rootURL)
    if bytes == -1:
        return newBytes, newLinks, newWords
    bytes = newBytes
    links = newLinks
    words = newWords
    
    # Crawl newly-returned URLs, making sure to keep track of which have been processed.
    for l in links:
        sleep(sleepTime)
        URL = l[0]
        if URL not in crawledLinks:
            crawledLinks.append(URL)
            newBytes, newLinks, newWords = crawlURL(URL)
            if newBytes >= 0:
                bytes += newBytes
                links.extend(newLinks)
                for w in newWords:
                    words[w] = words.get(w, 0) + newWords[w]

    return bytes, links, words

def analyzeStats(bytes, URLs, words):
    print("")

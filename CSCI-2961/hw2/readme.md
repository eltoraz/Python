`CLARIFICATIONS:

-- For crawling, you may decide to skip certain file types
   if you'd like (e.g. zip, pptx, ppt, etc.).  Or you may
   opt to crawl only certain file types (e.g. html, php,
   asp, aspx, jsp, etc.).  This is entirely optional; you
   may also simply crawl all pages regardless of file type.

-- Be sure that when you harvest URLs that you handle the
   following <a> tag formats for href:

    href="page3.html"
    href="subdir/page3.html"
    href="http://cnn.com/subdir/blah.html"

-- Be sure your function(s) return multiple values, where
   expected.  A Python function can return multiple values
   by doing this:

    return x, y, z
   
   The calling function "catches" these values via:

    a, b, c = somefunction()
   
   Do NOT use a list or other data structure to store and
   return all three values.  The above a, b, c approach
   must work.

-- As noted in the specifications, you can decide how to
   handle abbrevations, punctuation, etc.  In other words,
   you determine how to delimit words.

-- There is no need to validate HTML code (much of what's
   out there is not valid).  Do the best you can in parsing
   out <a> tags, etc.  Further, to capture the link text
   of an <a> tag, ignore other embedded tags; for
   example, given this tag:

    <a href="p.php"><b>click here</a>

   The link text is simply "click here" in this example.

-- Of course do not include any user interaction; and either
   comment out or remove any "main" code from your submission.

-- Be sure to match the output format and other specifications
   to the extent possible.`

Our second homework assignment is to be completed individually. Do not share code or review anyone else's code. Work on this homework assignment is to be your own.  
Submit your homework via [RPI LMS](https://rpilms.rpi.edu/webct/logon/200146816001). Put all your code into exactly one Python file and name it your RCS userid. For example, if your RCS userid is goldsd3, then your Python file name for this assignment must be `goldsd3.py`.  
*Be sure to comment your code and include your name at the top of each file submitted.*

**Web Page Crawl:**  
Write a Python function called `crawlURL()` that, given input string `URL`, retrieves the requested Web page and parses it. This function returns (in this order) the number of bytes retrieved (or -1 if an error occurs), a list of "harvested" URLs and their link-text, and a dictionary that maps words to word occurrence counts.  
To crawl a Web page, retrieve the page at the given URL. From the retrieved page, identify and isolate all links. You may assume that a link takes one of these forms in HTML:

`<a href="page1.html">Click here</a>
<a href="page2.html" otherstuff="..." ...>Also here</a>
<a otherstuff="..." href="http://cnn.com/another-page.html">Click here</a>
etc.`

Create a Python list of "harvested" URLs only for the given domain. In other words, if you are crawling `www.cs.rpi.edu`, only harvest URLs on that site. Ignore all others.  
In the list of harvested URLs, also record the corresponding link-text via a tuple. For example:
`[ ( 'http://www.cs.rpi.edu/page1.html', 'Click here' ), ( 'http://www.cs.rpi.edu/page2.html', 'Also here' ) ]`  
In addition to harvesting URLs, identify all unique words and their corresponding word occurrence counts. More specifically, remove all HTML tags and convert all text to lowercase. Further, use whatever approach you like to identifying valid words; think about what to do with punctuation, digits, etc.  
Store all words in a dictionary that identifies word counts, as in:  
`{ 'david':2, 'e':1, 'goldschmidt':10, 'phd':1, 'home':1, etc. }

# note that the ordering of the dictionary values certainly may vary!`

**Web Site Crawl:**  
To crawl an entire Web site, create a `crawlSite()` function that, given input string `rootURL`, repeatedly calls the `crawlURL()` function to obtain all linked pages rooted at `rootURL`. **Note that you should also implement a politeness policy that delays a few seconds between each page request!** Feel free to comment this politeness policy out when crawling sites you know can handle the traffic load.  
Typically, the `rootURL` is the host's domain name, as in `http://www.cs.rpi.edu/` or `http://www.rpi.edu/`. Also be sure that your function handles a root URL such as `http://cs.strose.edu/goldschd/`, indicating that we only want pages within the `goldschd` directory on the `cs.strose.edu` site.  
For each successive call to `crawlURL()`, keep a running total of the number of bytes read. Also merge the harvested URLs list and word occurrences map such that all pages are crawled only once. Note that you want to keep all link-text for harvested URLs.  
The `crawlSite()` function returns the same parameters as the `crawlURL()` function. More specifically, the `crawlSite()` function returns (in this order) the total number of bytes retrieved (ignoring pages with errors, which likely indicates a broken link), the unique list of "harvested" URLs and their link-text, and a dictionary that maps all words to overall word occurrence counts.


**Site Analysis:**
Using results from the above `crawlSite()` function, write a Python function called `analyzeStats()` that takes as input the three outputs of the `crawlSite()` function. Given these inputs, the `analyzeStats()` function must display the following information (using the format shown below). Be sure to sort the "URLs and Link-Text" output by URL. And sort the "Word Counts" by decreasing word occurrences. Further, be sure to format the columns such that they are uniform based on their longest entries (as shown below).

`total pages crawled successfully: 16
total words: 1073

URLs and Link-Text:
-------------------
http://cs.strose.edu/abc.php                ==>  'Neato script'
http://cs.strose.edu/longresourcename.html  ==>  'Check this out'
http://cs.strose.edu/page1.html             ==>  'Click here'
http://cs.strose.edu/page2.html             ==>  'Also here'
http://cs.strose.edu/page2.html             ==>  'Good stuff here'
etc.

Word Counts (total of 1073 words):
----------------------------------
of                ==>  286
and               ==>  277
the               ==>  251
goldschmidt       ==>  247   (okay, so this isn't real data!)
longestwordfound  ==>  186
etc.`

**Testing:**  
Test all of your functions carefully. Be sure your functions work for a variety of URLs, such as `http://www.cs.rpi.edu` and `http://cs.strose.edu/goldschd`.

**Extra Credit:**  
Graph the word count data by generating a JPG file called `wordcounts.jpg` in the current working directory. More specifically, the y-axis represents the word count, whereas the x-axis simply represents each word (from most frequently to least frequently occurring). This is essentially a scatter plot.
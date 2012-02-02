"""
Program:	bulkdownload.py
Author:		Bill Jameson (jamesw2@rpi.edu)
Description:	Bulk download files individually listed on a web page.
"""

import re
from urllib.request import Request, urlopen
from urllib.error import URLError
from time import sleep

baseurl = 'REPLACE THIS WITH THE PARENT DIRECTORY FOR THE FILES TO DOWNLOAD'
downloadspage = 'REPLACE THIS WITH THE PAGE LINKING TO THE FILES' 
regex = '<a.* href="REPLACE WITH THE FORMAT FOR THE LINKS YOU WANT TO GRAB, USING A REGEX TO MATCH THEM ALL">'

# get the list of MP3s
req = Request(downloadspage)
try:
    resp = urlopen(req)
except URLError as e:
    print('connection failed')

contents = resp.read().decode('utf-8')
files = re.findall(regex, contents)

# download the files
politeness = 2
for m in files:
    filename = m.replace('-', ' ').title() + '.EXT'
    url = downloadspage + '/' + m + '.EXT'
    f = open(filename, 'wb')
    try:
        remote = urlopen(url)
    except URLError as e:
        print('could not reach download page for file', filename)
        print(url)
        continue
        
    # This block is necessary for sites that link to a separate download page for each file.
    dlpagecontents = remote.read().decode('utf-8')
    dlkeyre = '<a.* href="REPLACE THIS WITH THE LINK FORMAT ON THE DOWNLOAD PAGE">REPLACE THIS WITH THE LINK TEXT FORMAT ON THE DOWNLOAD PAGE</a>'
    dlkey = re.search(dlkeyre, dlpagecontents).group(1)
    
    fileurl = baseurl + dlkey + '/' + m + '.EXT'
    
    try:
        remote = urlopen(fileurl)
    except URLError as e:
        print('connection for file', filename, 'failed')
        continue
    # [end block]
    
    print('downloading', filename + ',', 'filesize', remote.getheader('Content-Length'))
    contents = remote.read()
    f.write(contents)
    f.close()
    sleep(politeness)
    

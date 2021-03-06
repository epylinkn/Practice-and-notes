#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib
import shutil

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

def sort_key(url):
  match = re.search(r'-(\w+)-(\w+)\.\w+',url)
  if match:
    return match.group(2)
  else:
    return url

def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  # +++your code here+++

  # fines the index number for what matches the string '_'
  underbar = filename.index('_')
  # grabs what follows the '_'
  hostname = filename[underbar + 1:]

  result = []
  f = open(filename,'r')
  text = f.read()
  url = re.findall(r'GET (\S+puzzle\S+)' , text)

  for item in url:
    fullname = 'http://'+hostname+item
    if fullname not in result:
      result.append(fullname)
  f.close()
  #result.sort() 
  #for item in result:
    #print item
  return sorted(result, key=sort_key)

def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  # +++your code here+++
  if not os.path.exists(dest_dir):
    os.mkdir(dest_dir)
  #urllib.urlretrieve(img_urls)

  i=0
  f = open('index.html','w')
  f.write('<html><body>\n')
  for img in img_urls:
    toname = 'img%d'%i
    f.write('<img src=\"'+toname+'\">')
    #print 'Retrieving '+img+' and copying it as '+toname
    # urllib.urlretrieve takes 2 arguments: img_url, and where to copy as
    urllib.urlretrieve(img, os.path.join(dest_dir,toname))
    i+=1
  f.write('\n')
  f.write('</body></html>')
  f.close()
  shutil.move('index.html',dest_dir)
  

def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()

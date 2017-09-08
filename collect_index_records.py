import json
import requests
import codecs
import glob
import os
from utils import *


# First, get the CommonCrawl index records for each unique site, plus a couple extra
dir_path = os.path.dirname(os.path.realpath(__file__))
sites = ['testing.googleblog.com', 'theconversation.com', 'arstechnica.com', 'www.wired.com', 'dev.to', 
         'blog.openai.com', 'www.theatlantic.com', 'www.kurzweilai.net', 'www.theguardian.com', 'medium.com',
         'www.foxnews.com', 'www.breitbart.com']
archive_bucket = "CC-MAIN-2017-17-index"

for site in sites:
    print("Site: " + site)

    index_path = os.path.join(dir_path, 'data', 'index', site)
    if not os.path.exists(index_path):
        os.makedirs(index_path)
    
    num_pages = get_cc_index_num_pages(site + "/*", archive_bucket)
    print("Num pages: " + str(num_pages))

    filecount = 0
    for x in range(0, num_pages):
        print("Page " + str(x + 1) + " / " + str(num_pages))
        indexfilename = os.path.join(index_path, 'index_' + str(filecount) + '.json')
        filecount += 1
        if os.path.isfile(indexfilename):
            print("Already fetched, skipping")
            continue

        page = get_cc_index_records(site + "/*", archive_bucket, page=x)
        if len(page) == 1 and 'error' in page[0]:
            print("Error: " + page[0]['error'])
            continue

        with codecs.open(indexfilename, 'w', 'utf-8') as indexfile:
            json.dump(page, indexfile)

print("Done")
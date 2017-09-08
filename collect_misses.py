import json
import requests
import codecs
import glob
import os
import pypandoc
import random
import re
from bs4 import BeautifulSoup
from newspaper import Article
from utils import *

# List of sites and rules to exclude pages on those sites that aren't articles
sites = [
    { 'host': 'theconversation.com', 'exclude': '.+?(\/topics\/|\/columns|\/feeds|\/partners\/|robots.txt|\/fr|\/profiles\/)'},
    { 'host': 'testing.googleblog.com', 'include':'.+?\/\d{4}\/\d{2}\/.+' },
    { 'host': 'arstechnica.com', 'include':'.+?\/201[67]\/\d{2}\/[\w-]+' },
    { 'host': 'www.wired.com', 'include':'.+?com\/201[67]\/\d{2}\/[\w-]+' },
    { 'host': 'dev.to', 'include':'.+?dev.to\/(?!t\/).+?\/.+?' },
    { 'host': 'blog.openai.com', 'include':'.+?blog.openai.com\/(?!tag\/).+?\/' },
    { 'host': 'www.theatlantic.com', 'include':'.+?\/archive\/201[67]\/\d{2}\/.+?' },
    { 'host': 'www.kurzweilai.net', 'exclude':'.+?(\/page\/|robots.txt|\/feed|\/news\/)' },
    { 'host': 'www.theguardian.com', 'include':'.+?\/201[67]\/\w{3}\/\d{2}\/[\w-]+' },
    { 'host': 'medium.com', 'include':'.+?\/@.+?\/(?!(has-recommended|latest|following))[\w-]+' },
    { 'host': 'www.breitbart.com', 'include': '.+?com\/(?!(video)).+?\/201[67]\/\d{2}\/\d{2}\/[\w-]+' },
    { 'host': 'www.foxnews.com', 'include': '.+?\/201[67]\/\d{2}\/\d{2}\/[\w-]+' }
]
archive_bucket = "CC-MAIN-2017-17-index"

dir_path = os.path.dirname(os.path.realpath(__file__))
processed_path = os.path.join(dir_path, 'data', 'processed')

for site in sites:
    index_path = os.path.join(dir_path, 'data', 'index', site['host'])
    pages = load_index(index_path)

    print("Site: " + site['host'])
    print(("Total pages: " + str(len(pages))))

    # General exclusions
    pages = [x for x in pages if not re.match('.+?(.pdf$|robots.txt)', x['url'])]

    # Specific exclusions
    if 'exclude' in site:
        pages = [x for x in pages if not re.match(site['exclude'], x['url'])]
    elif 'include' in site:
        pages = [x for x in pages if re.match(site['include'], x['url'])]
    
    print(("Candidate pages: " + str(len(pages))))

    # Save the articles from a specific site into a folder for that site
    misses_path = os.path.join(dir_path, 'data', 'misses', site['host'])
    filecount = len(glob.glob(os.path.join(os.path.normpath(misses_path), '*.txt')))
    if filecount == 0:
        filecount = 1 
    sample_max = 100 - filecount + 1
    if len(pages) < sample_max:
        sample_size = len(pages)
    else:
        sample_size = sample_max

    # Save each of a random sample of articles to the site's folder
    for page in random.sample(pages, sample_size):
        print(page['url'])

        record = get_single_warcfile(page['filename'], page['offset'], page['length'])

        warc_record = get_record_with_header(
            record,
            header='WARC-Type',
            value='response'
        )

        article = Article(warc_record['WARC-Target-URI'])
        html = warc_record.payload.read()
        article.download(input_html=html)
        article.parse()

        content = re.sub(r'\n\s*\n', '\n\n', article.text)

        pub_date = ""
        if article.publish_date:
            pub_date = article.publish_date.strftime("%Y-%m-%d %H:%M:%S")

        # Add some metadata to the top of the article's file
        with codecs.open(os.path.join(misses_path, str(filecount) + '.txt'), 'w', 'utf-8') as outfile:
            outfile.write('---\n' + \
                        'Title: ' + article.title + '\n' + \
                        'PubDate: ' + pub_date + '\n' + \
                        'Author(s): ' + ', '.join(article.authors) + '\n' + \
                        '---\n' + \
                        content)
        filecount += 1


# Get a list of unique sites that I've saved articles from. That set will be used to get articles I *didn't* save

import codecs
import glob
import os
from urllib.parse import urlparse

dir_path = os.path.dirname(os.path.realpath(__file__))
source_path = os.path.join(dir_path, 'data', 'processed')

sites = set()

for filename in glob.glob(os.path.join(os.path.normpath(source_path), '*.txt')):
    with codecs.open(filename, "r", "utf-8") as fp:
        data = fp.read()
        meta = data.split('\n\n')
        sourcelines = list(filter(lambda x: x.startswith('Source:'), meta[1].split('\n')))
        if len(sourcelines) <= 0:
            continue
        source = sourcelines[0].split('Source:')[1]
        url_parts = urlparse(source)
        sites.add(url_parts.netloc)

print(sites)
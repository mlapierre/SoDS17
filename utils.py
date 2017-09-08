import requests
import gzip
import warc
import codecs
import glob
import os
import json
from urllib.parse import urlparse
from io import BytesIO
from io import StringIO
from clint.textui import progress

def get_single_warcfile(index_filename, offset, length, rec_type='warc'):
    # We need to calculate the start and the end of the relevant byte range
    # (each WARC file is composed of many small GZIP files stuck together)
    offset, length = int(offset), int(length)
    offset_end = offset + length - 1

    # We'll get the file via HTTPS so we don't need to worry about S3 credentials
    # Getting the file on S3 is equivalent however - you can request a Range
    prefix = 'https://commoncrawl.s3.amazonaws.com/'

    # We can then use the Range header to ask for just this set of bytes
    resp = requests.get(prefix + index_filename, headers={'Range': 'bytes={}-{}'.format(offset, offset_end)})

    # The page is stored compressed (gzip) to save space
    # We can extract it using the GZIP library
    raw_data = BytesIO(resp.content)
    f = gzip.GzipFile(fileobj=raw_data)

    # What we have now is just the WARC response, formatted:
    #data = f.read()
    
    #import pdb; pdb.set_trace()
    #return data.strip().split(bytes('\r\n\r\n', 'utf-8'), 2)
    return warc.WARCFile(fileobj=f, compress=False)

def get_record_with_header(warc_file, header, value):
    for record, _, _ in warc_file.browse():
        if record.header.get(header) == value:
            return record


def get_unique_sites_from_processed_notes(source_path):
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
            sites.add(url_parts.netloc.split(':')[0])

    return list(sites)

def get_cc_index_records(url_query, archive_bucket, page=0, pageSize=1):
    payload = { 'url': url_query, 'output' : 'json', 'page' : page, 'filter' : '!~filename:crawldiagnostics&mime:text/html&status:200' , 'pageSize': pageSize, 'from': '2016', 'to': '2017'}
    resp = requests.get('http://index.commoncrawl.org/' + archive_bucket, params=payload, stream=True)
    content = StringIO()
    for chunk in progress.dots(resp.iter_content(chunk_size=1024)):
        if chunk:
            content.write(chunk.decode('utf8'))
            content.flush()   
    return [json.loads(x) for x in content.getvalue().strip().splitlines()]

def get_cc_index_num_pages(url_query, archive_bucket):
    num_pages_payload = { 
        'url': url_query, 
        'output' : 'json', 
        'filter' : '!~filename:crawldiagnostics&mime:text/html&status:200' , 
        'pageSize': 1, 
        'from': '2016', 'to': '2017',
        'showNumPages': 'true'
        }
    resp = requests.get('http://index.commoncrawl.org/' + archive_bucket, params=num_pages_payload)
    resp_json = json.loads(resp.content.strip())
    #print(resp_json)
    return resp_json['pages']

def load_index(path):
    pages = []
    indexfilenames = glob.glob(os.path.join(path, 'index*.json'))
    for filename in indexfilenames:
        with codecs.open(filename, 'r', 'utf-8') as indexfile:
            pages += json.load(indexfile)
    return pages
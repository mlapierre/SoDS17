# 1. Export notes in Articles as HTML (excluding tag:twitter)
# 2. Move the html files to the 'interesting' folder (except Evernote_index)
# 3. Strip the html:

import codecs
import glob
import os
import pypandoc
from bs4 import BeautifulSoup

filecount = 1
for filename in glob.glob(os.path.join('data', 'interesting', '*.html')):
    with codecs.open(filename, "r", "utf-8") as fp:
        article = BeautifulSoup(fp, "html.parser")
        title = article.title.text
        meta = article.table.text.strip()

        # Structured content might be useful. For now, plain text
        content = article.find_all('div')[1].text
        #content = pypandoc.convert_text(article.find_all('div')[1], 'md', 'html')

        #print(title)
        #print(meta)
        #print(content)

        processed_path = os.path.join('data', 'processed')
        if (not os.path.isdir(processed_path)):
            os.mkdir(processed_path)
        
        with codecs.open(os.path.join(processed_path, str(filecount) + '.txt'), 'w', 'utf-8') as outfile:
            outfile.write('---\n' + \
                          'Title: ' + title + '\n' + \
                          meta + '\n' + \
                          '---\n' + \
                          content)
        filecount += 1

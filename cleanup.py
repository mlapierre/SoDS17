import codecs
import glob
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

# Get the titles of the hits
hits_titles = []
hits_path = os.path.join(dir_path, 'data', 'to_analyse', 'hits')
for filename in glob.glob(os.path.join(os.path.normpath(hits_path), '*.txt')):
    with codecs.open(filename, "r", "utf-8") as fp:
        data = fp.read()
        _, meta, content = data.split('---\n', maxsplit=2)
        sourcelines = meta.split('\n')
        if len(sourcelines) <= 0:
            continue
        title = sourcelines[0].split('Title:')[1].strip()
        hits_titles.append(title)

to_delete = []
misses_path = os.path.join(dir_path, 'data', 'to_analyse', 'misses')
for filename in glob.glob(os.path.join(os.path.normpath(misses_path), '*.txt')):
    with codecs.open(filename, "r", "utf-8") as fp:
        data = fp.read()
        _, meta, content = data.split('---\n', maxsplit=2)

        # Delete the file if the content is too short
        if len(content) < 1000:
            print("deleting {} because the content is < 1000 characters".format(filename))
            to_delete.append(filename)
            continue

        sourcelines = meta.split('\n')
        if len(sourcelines) <= 0:
            continue
        
        # Delete the file if the title is the same as a hit
        title = sourcelines[0].split('Title:')[1].strip()
        if title in hits_titles:
            print("deleting {} because it's title is a hit: {}".format(filename, title))
            to_delete.append(filename)
            continue

for filename in to_delete:
    os.remove(filename)

print("Done")
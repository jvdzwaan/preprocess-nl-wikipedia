"""Script to extract articles from wikipedia dump and store cleaned text

An article is stored on a single line. Output files are approximately 10Mb
each.

Usage: python dump2txt.py <dump file> <output dir>
"""
from lxml import etree
from bz2 import BZ2File
import sys
from mw2txt import get_siteinfo, dispatch_text, parse
import os
import itertools
import codecs
import shutil
import multiprocessing as mp
import time

def get_articles_test(q, dump, num_workers):
    print 'Ja'
    for s in ["abc", "[[Abc][abc]]", "===Heading==="]:
        print 'loop'
        q.put(s)
    for i in range(num_workers):
        q.put('END')

def get_articles(queue, wp_dump, num_workers):
    page_tag = '{http://www.mediawiki.org/xml/export-0.10/}page'
    text_tag = '{http://www.mediawiki.org/xml/export-0.10/}text'
    title_tag = '{http://www.mediawiki.org/xml/export-0.10/}title'
    revision_tag = '{http://www.mediawiki.org/xml/export-0.10/}revision'
    ns_tag = '{http://www.mediawiki.org/xml/export-0.10/}ns'
   
    with BZ2File(wp_dump) as xml_file:
        context = etree.iterparse(xml_file, events=('end',), tag=page_tag)
        for event, elem in context:
            # check if the page is a regular article
            if elem.find(ns_tag).text != '0':
                continue
         
            title = elem.find(title_tag).text
            #print 'Adding', title
            #print 'Queue size:', queue.qsize()
            text = elem.find('{}/{}'.format(revision_tag, text_tag)).text
            while True:
                if queue.qsize() > 2500:
                    time.sleep(1)
                else:
                    break
            queue.put(u'{} {}\n'.format(title,
                                        text))
    for i in range(num_workers):
        queue.put(u'END')

def clean_wiki_text(q_in, q_out):
    while True:
        text = q_in.get()
        if text == 'END':
            q_out.put(text)
            break
        else:
            dispatcher, sep = dispatch_text, u""
            si = get_siteinfo('nl')
            res = parse(text, siteinfo=si)
            output = sep.join("_".join(e for e in i) for i in dispatcher(res))
            output = output.replace('\n', ' ')
            #print 'parsed text'
            q_out.put(output)


def write2file(queue, wp_dump):
    out_file_number = 1
    num_articles = 0
    fname = os.path.basename(wp_dump).replace('.xml.bz2', '')

    out_file = os.path.join(out_dir, '{}-{}.txt'.format(fname,
                            str(out_file_number).zfill(3)))
    while True:
        text = queue.get()
        if text == 'END':
            break
        else:
            num_articles = num_articles + 1
            out_file = os.path.join(out_dir, '{}-{}.txt'.format(fname,
                                    str(out_file_number).zfill(3)))
            with codecs.open(out_file, 'ab', 'utf-8') as f:
                f.write(u'{}\n'.format(text))
            if os.path.getsize(out_file) > 10 * 1024 * 1024:
                print 'wrote {} articles to {}'.format(num_articles, out_file)
                out_file_number = out_file_number + 1
                num_articles = 0


wp_dump = sys.argv[1]
out_dir = sys.argv[2]

try: 
    shutil.rmtree(out_dir)
except OSError:
    pass
finally:
    os.makedirs(out_dir)

num_workers = 12 

texts = mp.Queue()
dump2articles = mp.Process(target=get_articles, args=(texts, wp_dump,
                                                      num_workers))
dump2articles.start()

clean_texts = mp.Queue()
for x in range(num_workers):
    worker = mp.Process(target=clean_wiki_text, args=(texts, clean_texts))
    worker.start()

write_output = mp.Process(target=write2file, args=(clean_texts, wp_dump))
write_output.start()

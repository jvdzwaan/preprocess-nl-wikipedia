from lxml import etree
from bz2 import BZ2File
import sys
from mw2txt import get_siteinfo, dispatch_text, parse
import os
import itertools
import codecs
import shutil

wp_dump = sys.argv[1]
out_dir = sys.argv[2]

try: 
    shutil.rmtree(out_dir)
    os.makedirs(out_dir)
except OSError:
    os.makedirs(out_dir)

page_tag = '{http://www.mediawiki.org/xml/export-0.10/}page'
text_tag = '{http://www.mediawiki.org/xml/export-0.10/}text'
title_tag = '{http://www.mediawiki.org/xml/export-0.10/}title'
revision_tag = '{http://www.mediawiki.org/xml/export-0.10/}revision'
ns_tag = '{http://www.mediawiki.org/xml/export-0.10/}ns'
    
si = get_siteinfo('nl')
dispatcher, sep = dispatch_text, '' 

out_file_number = 1
num_articles = 0
fname = os.path.basename(wp_dump).replace('.xml.bz2', '')

with BZ2File(wp_dump) as xml_file:
    context = etree.iterparse(xml_file, events=('end',), tag=page_tag)
    for event, elem in context:
        # check if the page is a regular article
        if elem.find(ns_tag).text != '0':
            continue
        num_articles = num_articles + 1
        title = elem.find(title_tag).text
        text = elem.find('{}/{}'.format(revision_tag, text_tag)).text
        #print u'processing article: {}'.format(title).encode('utf-8')
        try:
            res = parse(text, siteinfo=si)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            sys.exit()
        output = sep.join("_".join(e for e in i) for i in dispatcher(res))
        output = output.replace('\n', ' ')

        out_file = os.path.join(out_dir, '{}-{}.txt'.format(fname,
                                str(out_file_number).zfill(3)))
        with open(out_file, 'ab') as f:
            f.write('{} {}\n'.format(title.encode('utf-8'), output.encode('utf-8')))
        if os.path.getsize(out_file) > 1 * 1024 * 1024:
            print 'wrote {} articles'.format(num_articles)
            out_file_number = out_file_number + 1
            print 'writing text to', os.path.join(out_dir,
                   '{}-{}.txt'.format(fname, str(out_file_number).zfill(3)))
            num_articles = 0

import sys
import os
import glob
import codecs
from bs4 import BeautifulSoup
import logging
import time

#from cptm.utils.frog import get_frogclient, pos_and_lemmas
#from cptm.utils.inputgeneration import remove_trailing_digits


def process_file(xml_file, output_dir, frogclient=None):
    n_texts = 0

    #start = time.time()
    p, n = os.path.split(xml_file)
    d = p.rsplit('/')[-1]
    output_dir = os.path.join(output_dir, d)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    out_file = os.path.join(output_dir,
                            os.path.basename(xml_file))

    with codecs.open(xml_file, 'rb', 'utf-8') as f:
        soup = BeautifulSoup(f.read(), 'lxml')

    docs = soup.find_all('doc')
    #logger.info('found {} articles'.format(len(docs)))
    with codecs.open(out_file, 'wb', 'utf-8') as f:
        for i, doc in enumerate(docs):
            #lemmas = []
            lines = doc.text.split('\n')
            #print '({} of {}) {}'.format(i+1, len(docs), lines[1].encode('utf-8')),
            #print '{} lines'.format(len(lines)),
            #print len(doc)
            if len(doc) > 1:
                #print doc
                print '{} in "{} ({} docs)"'.format(lines[1].encode('utf-8'), xml_file, len(doc))
                #docs2 = doc.find_all('doc')
                #print len(docs2)
                #doc = docs2[0]
                #print doc
                time.sleep(3)

            #for j, line in enumerate(lines):
                #print '{} lines'.format(len(lines))
                #if len(lines)>1000:
                #    print doc.text
                #not_parsed = True
                #while not_parsed:
                #    try:
                #        parsed = pos_and_lemmas(line, frogclient)
                #        not_parsed = False
                #    except Exception, e:
                #        logger.warn(str(e))
                #        del frogclient
                #        frogclient = get_frogclient()

                #for pos, lemma in parsed:
                #    lemmas.append(remove_trailing_digits(lemma))
                #print lemmas
            #f.write(' '.join(lemmas)+'\n')
            #n_texts = n_texts + 1
        #end = time.time()

    #print 'Done with {} ({} sec)'.format(xml_file, (end-start))
    return n_texts


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

input_dir = sys.argv[1]
output_dir = sys.argv[2]

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

#frog_client = get_frogclient()

input_files = glob.glob('{}/**/wiki*'.format(input_dir))
input_files.sort()
#logger.info('lemmatizing text in {} files'.format(len(input_files)))

num_texts = 0

for i, f in enumerate(input_files):
    #logger.info('processing file {} (#{})'.format(f, i))
    num_texts += process_file(f, output_dir)
#logger.info('lemmatized {} texts'.format(num_texts))

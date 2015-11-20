# -*- coding: utf-8 -*-
"""Preprocessing texts for topic coherence calculation
"""
import glob
import codecs
import os
import time
from pattern.nl import parsetree
from multiprocessing import Pool
from bs4 import BeautifulSoup
import sys
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def lemmatize(text):
    r = parsetree(text,
                  tokenize=True,     # Split punctuation marks from words?
                  tags=True,         # Parse part-of-speech tags? (NN, JJ, ...)
                  chunks=False,      # Parse chunks? (NP, VP, PNP, ...)
                  relations=False,   # Parse chunk relations? (-SBJ, -OBJ, ...)
                  lemmata=True,      # Parse lemmata? (ate => eat)
                  encoding='utf-8',  # Input string encoding.
                  tagset=None)       # Penn Treebank II (default) or UNIVERSAL.

    words = []
    for sentence in r:
        for lemma in sentence.lemmata:
            words.append(lemma)
    return words


def process_file(xml_file, output_dir):
    n_texts = 0

    try:
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
        with codecs.open(out_file, 'wb', 'utf-8') as f:
            for doc in docs:
                lemmas = lemmatize(doc.text.replace('\n', ' '))
                f.write(' '.join(lemmas)+'\n')
                n_texts = n_texts + 1
        #end = time.time()
    except Exception, e:
        logger.error('Failed to open file', exc_info=True)
    #print 'Done with {} ({} sec)'.format(xml_file, (end-start))
    return n_texts

input_dir = sys.argv[1]
output_dir = sys.argv[2]

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

input_files = glob.glob('{}/**/wiki*'.format(input_dir))
logger.info('lemmatizing text in {} files'.format(len(input_files)))

pool = Pool()
results = [pool.apply_async(process_file, args=(f, output_dir))
           for f in input_files]

pool.close()
pool.join()
output = [p.get() for p in results if p is not None and p.get() is not None]

logger.info('{} of files successfully processed'.format(len(output)))
logger.info('{} articles found'.format(np.sum(output)))

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
            if not lemma == 'http:':
                words.append(lemma)
                #print lemma
    return words


def process_file(xml_file, output_dir):
    start = time.time()
    p, n = os.path.split(xml_file)
    d = p.rsplit('/')[-1]
    #print d
    output_dir = os.path.join(output_dir, d)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    out_file = os.path.join(output_dir,
                            os.path.basename(xml_file).replace('xml', 'txt'))
    with codecs.open(xml_file, 'rb', 'utf-8') as f:
        soup = BeautifulSoup(f.read(), 'lxml')

    docs = soup.find_all('doc')
    with codecs.open(out_file, 'wb', 'utf-8') as f:
        for doc in docs:
            lemmas = lemmatize(doc.text.replace('\n', ' '))
            f.write(' '.join(lemmas)+'\n')
    end = time.time()
    print 'Done with {} ({} sec)'.format(xml_file, (end-start))

input_dir = sys.argv[1]
output_dir = sys.argv[2]

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

input_files = glob.glob('{}/**/wiki*'.format(input_dir))
pool = Pool()
results = [pool.apply_async(process_file, args=(f, output_dir))
           for f in input_files]

pool.close()
pool.join()

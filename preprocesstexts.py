# -*- coding: utf-8 -*-
"""Preprocessing texts for topic coherence calculation
"""
import glob
import codecs
import uuid
import os
import tarfile
import string
import time
from pattern.nl import parsetree
import shutil
from multiprocessing import Pool

def articles(txt_file):
    with codecs.open(txt_file, 'rb', 'utf-8') as f:
        text = f.read()
        articles = text.split('\n\n[[')
        for article in articles:
            yield article


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


def process_file(txt_file, output_dir):
    start = time.time()
    out_file = os.path.join(output_dir, os.path.basename(txt_file))
    with codecs.open(out_file, 'wb', 'utf-8') as f:
        for article in articles(txt_file):
            article = article.replace('[', '')
            article = article.replace(']', '')
            article = article.replace('=', ' ')
            article = article.replace('*', ' ')
            article = article.replace('\'\'', ' ')
            article = article.replace('"', ' ')
            article = article.replace('|', ' ')
            article = article.replace('\n', ' ')

            words = lemmatize(article)

            f.write(' '.join(words)+'\n')
    end = time.time()
    print 'Done with {} ({} sec)'.format(txt_file, (end-start))

input_dir = '/home/jvdzwaan/data/wikipedia-text/'
output_dir = '/home/jvdzwaan/data/wikipedia-articles/'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

text_files = glob.glob('{}*.txt'.format(input_dir))
pool = Pool()
results = [pool.apply_async(process_file, args=(txt_file, output_dir))
           for txt_file in text_files]

pool.close()
pool.join()

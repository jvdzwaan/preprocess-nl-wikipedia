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
            if not lemma in string.punctuation and not lemma == 'http:':
                words.append(lemma)
                #print lemma
    return words


input_dir = '/home/jvdzwaan/data/wikipedia-text-sample/'
output_dir = '/home/jvdzwaan/data/wikipedia-articles/'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

text_files = glob.glob('{}*.txt'.format(input_dir))
for i, txt_file in enumerate(text_files):
    print '{} ({} of {})'.format(txt_file, i+1, len(text_files)),

    out_file = os.path.join(output_dir, os.path.basename(txt_file))
    start = time.time()
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
    print ' -> {} sec'.format(end-start)

    #print repr(txt)


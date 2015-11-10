# -*- coding: utf-8 -*-
"""Preprocessing texts for topic coherence calculation
"""
import glob
import codecs
import uuid
import os
import tarfile
from pattern.nl import parsetree


def articles(input_dir):
    text_files = glob.glob('{}*.txt'.format(input_dir))
    for txt_file in text_files:
        with codecs.open(txt_file, 'rb', 'utf-8') as f:
            text = f.read()
            articles = text.split('\n\n[[')
            for article in articles:
                yield article

input_dir = '/home/jvdzwaan/data/wikipedia-text-sample/'
output_dir = '/home/jvdzwaan/data/wikipedia-articles/'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for article in articles(input_dir):
    article = article.replace('[[', '')
    article = article.replace(']]', '')

    out_file = os.path.join(output_dir, str(uuid.uuid4()))
    with codecs.open(out_file, 'wb', 'utf-8') as f:
        f.write(article)

    #txt = parsetree(article,
    #                tokenize=True,     # Split punctuation marks from words?
    #                tags=True,         # Parse part-of-speech tags? (NN, JJ, ...)
    #                chunks=False,      # Parse chunks? (NP, VP, PNP, ...)
    #                relations=False,   # Parse chunk relations? (-SBJ, -OBJ, ...)
    #                lemmata=True,      # Parse lemmata? (ate => eat)
    #                encoding='utf-8',  # Input string encoding.
    #                tagset=None)       # Penn Treebank II (default) or UNIVERSAL.

    #print repr(txt)


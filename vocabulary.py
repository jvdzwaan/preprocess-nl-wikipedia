"""Script to extract vocabulary from lemmatized wikipedia

Uses gensim

Perhaps the number of tokens in the vocabulary should be tweaked (it now throws
away a lot of words).

The resulting dictionary can be used to compare the vocabularies of lemma's
from frog (Dutch Dilipad data) and pattern (nlwikipedia data).
"""
from gensim.corpora import Dictionary
import sys
import glob
import codecs
import logging
import os

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)

input_dir = sys.argv[1]
output_dir = sys.argv[2]

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

input_files = glob.glob('{}/**/wiki*'.format(input_dir))

vocabulary = Dictionary(line.lower().split()
                        for f in input_files
                        for line in codecs.open(f, 'r', encoding='utf-8'))

vocabulary.save('{}/pattern_lemmas.dict'.format(output_dir))

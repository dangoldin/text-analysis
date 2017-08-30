#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
from collections import Counter, defaultdict

from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

from textstat.textstat import textstat

stop = set(stopwords.words('english'))

def print_spacing(text, spacing = ''):
    print spacing, text

def read_file(file):
    with open(file, 'r') as f:
        return f.read()

def get_sentences(text):
    return sent_tokenize(text.decode('utf-8'))

def get_words(text):
    return [w.lower() for w in re.findall(r'\w+', text) if w.lower()]

def get_num_words(text):
    return len(get_words(text))

def get_word_stats(words):
    s = sum([len(w) for w in words])
    print 'Average word length:', 1.0 * s/len(words)

    c = Counter(words)
    print 'Most common words:', c.most_common(20)

    c2 = Counter(zip(words, words[1:]))
    print 'Most common word pairs:', c2.most_common(20)

    longest = sorted(list(set(words)), key=lambda w: len(w), reverse=True)
    print 'Longest words:', longest[:20]
    print 'Unique words:', len(set(words))
    print 'Unique word density:', 1.0*len(set(words))/len(words)

def get_sentence_stats(sentences):
    print 'Num sentences:', len(sentences)
    print 'Average sentence length - chars:', 1.0*sum(len(s) for s in sentences)/len(sentences)
    print 'Average sentence length - words:', 1.0*sum(get_num_words(s) for s in sentences)/len(sentences)

if __name__ == '__main__':
    FILES_OR_DIRS = sys.argv[1:]

    WORD_SETS = defaultdict(set)
    for FILE_OR_DIR in FILES_OR_DIRS:
        if os.path.isdir(FILE_OR_DIR):
            FILES = [os.path.join(FILE_OR_DIR, fn) for fn in os.listdir(FILE_OR_DIR)]
        else:
            FILES = [FILE_OR_DIR]

        for FILE in FILES:
            print 'Processing', FILE
            TEXT = read_file(FILE)

            print 'Flesh reading ease', textstat.flesch_reading_ease(TEXT)
            print 'Smog index', textstat.smog_index(TEXT)
            print 'Flesch Kincaid grade', textstat.flesch_kincaid_grade(TEXT)
            print 'Coleman Liau', textstat.flesch_kincaid_grade(TEXT)
            print 'Automated readability index', textstat.automated_readability_index(TEXT)
            print 'Dale Chall readability score', textstat.dale_chall_readability_score(TEXT)
            print 'Difficult words', textstat.difficult_words(TEXT)
            print 'Linsear write formula', textstat.linsear_write_formula(TEXT)
            print 'Gunning fog', textstat.gunning_fog(TEXT)
            print 'Text standard', textstat.text_standard(TEXT)

            print '\nWords'
            WORDS = get_words(TEXT)
            get_word_stats(WORDS)

            print '\nWords no Stop Words'
            WORDS_NO_STOP = [w for w in WORDS if w not in stop]
            get_word_stats(WORDS_NO_STOP)

            print '\nSentences'
            SENTENCES = get_sentences(TEXT)
            get_sentence_stats(SENTENCES)
            print

            WORD_SETS[FILE_OR_DIR] |= set(WORDS)

    for FILE_OR_DIR1 in FILES_OR_DIRS:
        for FILE_OR_DIR2 in FILES_OR_DIRS:
            if FILE_OR_DIR1 != FILE_OR_DIR2:
                print FILE_OR_DIR1, 'vs', FILE_OR_DIR2
                print WORD_SETS[FILE_OR_DIR1] - WORD_SETS[FILE_OR_DIR2]

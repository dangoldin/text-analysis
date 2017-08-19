#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
from collections import Counter
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

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
    FILES = sys.argv[1:]

    WORD_SETS = {}
    for FILE in FILES:
        print 'Processing', FILE
        TEXT = read_file(FILE)

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

        WORD_SETS[FILE] = set(WORDS)

    for FILE1 in FILES:
        for FILE2 in FILES:
            if FILE1 != FILE2:
                print FILE1, 'vs', FILE2
                print WORD_SETS[FILE1] - WORD_SETS[FILE2]

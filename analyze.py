#!/usr/bin/env python

import sys
import re
from collections import Counter

def read_file(file):
    with open(file, 'r') as f:
        return f.read()

def get_words(text):
    return [w.lower() for w in re.findall(r'\w+', text)]

def get_stats(words):
    s = sum([len(w) for w in words])
    print 1.0 * s/len(words)

    c = Counter(words)
    print c.most_common(20)

    longest = sorted(list(set(words)), key=lambda w: len(w), reverse=True)
    print longest[:20]

if __name__ == '__main__':
    files = sys.argv[1:]

    for file in files:
        print 'Processing', file
        text = read_file(file)
        words = get_words(text)
        get_stats(words)

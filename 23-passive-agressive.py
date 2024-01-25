#!/usr/bin/env python

import sys, re, operator, string, traceback

def extract_words(path_to_file):
    assert(type(path_to_file) is str), "I need a string for an input text file"
    assert(path_to_file), "Please pass an input text file"

    with open(path_to_file) as f:
        str_data = f.read()

    pattern = re.compile('[\W_]+')
    word_list = pattern.sub(' ',str_data).lower().split()
    return word_list

def remove_stop_words(word_list):
    assert(type(word_list) is list), "Please pass a list"

    with open('./stop_words.txt') as f:
        stop_words = f.read().split(',')

    stop_words.extend(list(string.ascii_lowercase))
    return [w for w in word_list if not w in stop_words]

def frequencies(word_list):
    assert(type(word_list) is list), "Please pass a list"
    assert(word_list != []), "Please pass a non-empty list"

    word_freqs = {}
    for w in word_list:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1

    return word_freqs

def sort(word_freqs):
    assert(type(word_freqs) is dict), "Please pass a dictionary"
    assert(word_freqs != {}), "Please pass a non-empty dictionary"

    return sorted(word_freqs.items(), key=operator.itemgetter(1), reverse=True)

try:
    assert(len(sys.argv) > 1), "Please set an input text file"
    word_freqs = sort(frequencies(remove_stop_words(extract_words(sys.argv[1]))))

    assert(len(word_freqs) > 25), "Word frequency list is less than 25"
    for (w, c) in word_freqs[0:25]:
        print(w, '-', c)

except Exception as e:
    print("Something wrong: {0}".format(e))
    traceback.print_exc()

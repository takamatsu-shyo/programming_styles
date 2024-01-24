#!/usr/bin/env python

import sys, re, operator, string, traceback

def extract_words(path_to_file):
    assert(type(path_to_file) is str), "I need a string for an input text file"
    assert(path_to_file), "Please pass an input text file"

    try:
        with open(path_to_file) as f:
            str_data = f.read()
    except OSError as e:
        print("OS error({0}) when opening {1}: {2}! Quiting".format(e.errorno, path_to_file, e.strerror))
        raise e

    pattern = re.compile('[\W_]+')
    word_list = pattern.sub(' ',str_data).lower().split()
    return word_list

def remove_stop_words(word_list):
    assert(type(word_list) is list), "Please pass a list"

    try:
        with open('./stop_words.txt') as f:
            stop_words = f.read().split(',')
    except OSError as e:
        print("OS error({0}) when opening ./stop_words.txt: {1}! Quiting".format(e.errorno, e.strerror))
        raise e

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

    try:
        return sorted(word_freqs.items(), key=operator.itemgetter(1), reverse=True)
    except Exception as e:
        print("Sorted threw {0}".format(e))
        raise e

try:
    assert(len(sys.argv) > 1), "Please set an input text file"
    word_freqs = sort(frequencies(remove_stop_words(extract_words(sys.argv[1]))))

    assert(type(word_freqs) is list), "Plase set a list"
    assert(len(word_freqs) > 25), "Word frequency list is less than 25"
    for (w, c) in word_freqs[0:25]:
        print(w, '-', c)

except Exception as e:
    print("Something wrong: {0}".format(e))
    traceback.print_exc()

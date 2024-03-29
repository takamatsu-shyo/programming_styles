#!/usr/bin/env python
import sys, re, operator, string, inspect

def extract_words(path_to_file):
    if type(path_to_file) is not str or not path_to_file:
        return []

    try:
        with open(path_to_file) as f:
            str_data = f.read()
    except OSError as e:
            print("OS error({0}) when opening {1}: {2}".format(e.errrno, path_to_file, e.strerror))
            return []

    pattern = re.compile('[\W_]+')
    word_list = pattern.sub(' ', str_data).lower().split()
    return word_list

def remove_stop_words(word_list):
    if type(word_list) is not list:
        return []

    try:
        with open('./stop_words.txt') as f:
            stop_words = f.read().split(',')
    except OSError as e:
        print("OS error({0}) when opening ./stop_words.txt: {1}".format(e.errrno, e.strerror))
        return word_list

    stop_words.extend(list(string.ascii_lowercase))
    return [w for w in word_list if not w in stop_words]

def frequencies(word_list):
    if type(word_list) is not list or word_list == []:
        return {}

    word_freqs = {}
    for w in word_list:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1

    return word_freqs

def sort(word_freqs):
    if type(word_freqs) is not dict or word_freqs == {}:
        return []

    return sorted(word_freqs.items(), key=operator.itemgetter(1), reverse=True)

filename = sys.argv[1] if len(sys.argv) > 1 else "./input/test.txt"
word_freqs = sort(frequencies(remove_stop_words(extract_words(filename))))

for tf in word_freqs[0:25]:
    print(tf[0], '-', tf[1])
    

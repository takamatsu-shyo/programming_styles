#!/usr/bin/env python
import sys, re, operator, string

def read_file(input_file):
    with open(input_file) as f:
        data = f.read()
    return data

def filter_and_normalize(input_string):
    pattern = re.compile('[\W_]+')
    return pattern.sub(' ', input_string).lower()

def make_list(input_string):
    return input_string.split()

def remove_stop_words(word_list):
    with open('stop_words.txt') as f:
        stop_words = f.read().split(',')

    stop_words.extend(list(string.ascii_lowercase))
    return [w for w in word_list if w not in stop_words]

def frequency(word_list):
    word_freq = {}
    for word in word_list:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1

    return word_freq

def sort(word_freq):
    return sorted(word_freq.items(), key=operator.itemgetter(1), reverse=True)

def print_all(word_freq):
    if (len(word_freq) > 0):
        print(word_freq[0][0], '-', word_freq[0][1])
        print_all(word_freq[1:])

print_all(sort(frequency(remove_stop_words(make_list(filter_and_normalize(read_file(sys.argv[1]))))))[0:25])

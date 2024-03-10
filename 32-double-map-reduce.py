#!/usr/bin/env python:
import sys, re, operator, string
from functools import reduce

def splitter(input_string, number_lines):
	"""
	Partition the input input_string
	into to chunk of number_lines
	"""
	lines = input_string.split('\n')
	for i in range(0, len(lines), number_lines):
		yield '\n'.join(lines[i:i+number_lines]	)

def generate_wordlist(input_string):
	"""
	Take a string, returng a list of paris (word, 1),
	one for each word in the input, so
	[(wq, 1), (w2, 1), ... (wn, 1)]
	"""
	def _scan(string_data):
		pattern = re.compile('[\W_]+')
		return pattern.sub(' ', string_data).lower().split()

	def _remove_stop_words(word_list):
		with open('./stop_words.txt') as f:
			stop_words = f.read().split(',')
		stop_words.extend(list(string.ascii_lowercase))
		return [w for w in word_list if not w in stop_words]

	result = []
	words = _remove_stop_words(_scan(input_string	))
	for w in words:
		result.append((w, 1))
	return result

def group_again(input_list):
	mapping = {}
	for pairs in input_list:
		for p in pairs:
			if p[0] in mapping:
				mapping[p[0]].append(p)
			else:
				mapping[p[0]] = [p]
	return mapping

def word_count(mapping):
	def add(x, y):
		return x+y

	return (mapping[0], reduce(add, (pair[1] for pair in mapping[1])))

def read_file(path_to_file):
	with open(path_to_file) as f:
		data_str	 = f.read()
	return data_str

def sort(word_freq):
	return sorted(word_freq, key=operator.itemgetter(1), reverse=True)

splits = map(generate_wordlist, splitter(read_file(sys.argv[1]), 200))
splits_per_word = group_again(splits)
word_frequency = sort(map(word_count, splits_per_word.items()))

for (w, c) in word_frequency[0:25]:
	print(w, '-', c)
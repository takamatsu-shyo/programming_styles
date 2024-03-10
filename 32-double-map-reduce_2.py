#!/usr/bin/env python
import sys, re, operator, string
from functools import reduce

def splitter(input_string, line_number):
	input_line = input_string.split('\n')
	for i in range(0, len(input_line), line_number):
		yield '\n'.join(input_line[i:i+line_number])

def word_splitter(input_string):
	def _scanner(coming_string):
		compiled_pattern = re.compile('[\W_]+')
		return compiled_pattern.sub(' ', coming_string).lower().split()

	def _removing_stop_word(input_word_list):
		with open('./stop_words.txt') as f:
			stopping_word = f.read().split(',')
		stopping_word.extend(list(string.ascii_lowercase))
		return [w for w in input_word_list if not w in stopping_word]

	result_list = []
	output_words = _removing_stop_word(_scanner(input_string))
	for w in output_words:
		result_list.append((w, 1))
	return result_list

def regrouping(paired_list):
	the_map = {}
	for pairs in paired_list:
		for p in pairs:
			if p[0] in the_map:
				the_map[p[0]].append(p)
			else:
				the_map[p[0]] = [p]
	return the_map

def words_counter(input_map):
	def adding(x, y):
		return x+y

	return (input_map[0], reduce(adding, (p[1] for p in input_map[1])))


def reading_file(input_file):
	with open(input_file) as f:
		data = f.read()
	return data

def sorting(word_frequency):
	return sorted(word_frequency, key=operator.itemgetter(1), reverse=True)

parted = map(word_splitter, splitter(reading_file(sys.argv[1]), 200))
parted_per_word = regrouping(parted)
word_frequency = sorting(map(words_counter, parted_per_word.items()))

for (w, c) in word_frequency[0:25]:
	print(w, '-', c)

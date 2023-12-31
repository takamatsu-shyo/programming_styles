#!/usr/bin/env python
import abc, sys, re, operator, string

class IDataStroage (metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def words(self):
        pass

class IStopWordFilter (metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def is_stop_word(self, word):
        pass

class IWordFresuencyCounter(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def increment_count(self, word):
        pass

    @abc.abstractmethod
    def sorted(self):
        pass

class DataStroageManager:
    _data = ''
    def __init__(self, path_to_file):
        with open(path_to_file) as f:
            self._data = f.read()
        pattern = re.compile('[\W_]+')
        self._data = pattern.sub(' ', self._data).lower()
        self._data = ''.join(self._data).split()

    def words(self):
        return self._data

class StopWordManager:
    _stop_words = []
    def __init__(self):
        with open('./stop_words.txt') as f:
            self._stop_words = f.read().split(',')
        self._stop_words.extend(list(string.ascii_lowercase))

    def is_stop_word(self, word):
        return word in self._stop_words

class WordFrequencyManager:
    _word_freqs = {}

    def increment_count(self, word):
        if word in self._word_freqs:
            self._word_freqs[word] += 1
        else:
            self._word_freqs[word] = 1

    def sorted(self):
        return sorted(self._word_freqs.items(), key=operator.itemgetter(1), reverse=True)

IDataStroage.register(subclass=DataStroageManager)
IStopWordFilter.register(subclass=StopWordManager)
IWordFresuencyCounter.register(subclass=WordFrequencyManager)

class WordFrequencyController:
    def __init__(self, path_to_file):
        self._storage = DataStroageManager(path_to_file)
        self._stop_words_manager = StopWordManager()
        self._word_freqs_counter = WordFrequencyManager()

    def run(self):
        for w in self._storage.words():
            if not self._stop_words_manager.is_stop_word(w):
                self._word_freqs_counter.increment_count(w)

        word_freqs = self._word_freqs_counter.sorted()
        for (w, c) in word_freqs[0:25]:
            print(w, '-', c)

WordFrequencyController(sys.argv[1]).run()

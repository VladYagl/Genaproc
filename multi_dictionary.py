import random
import string
import nltk

from typing import Dict, List
from nltk import tokenize
from functional import compose, partial


def h(l: List[str]):
    return (''.join(map(str.strip, l))).lower()


# TODO: keep original capitalisation
# TODO private
class MultiDictionary:
    class Word:
        def __init__(self, prefix: List[str]):
            self.prefix = prefix
            self.clean = list(map(compose(str.strip, str.lower), prefix))
            self.next = {}
            self.count = 0
            self.as_first = 0
            self.as_last = 0

        def __str__(self):
            return "str " + self.__repr__()

        def __repr__(self):
            return str(self.prefix)  # + " #" + str(self.count) # + " -> " + str(self.next)

        def __lt__(self, other):
            return (self.as_first, self.count) < (other.as_first, other.count)

        def add(self, word):
            if word not in self.next:
                self.next[word] = 0
            self.next[word] += 1

    def __init__(self, prefix_size, file):
        self.__data: Dict[str, MultiDictionary.Word] = {}
        self.prefix_size = prefix_size
        self.word_count = 0
        self.learn(file)
        self.current = []
        self.dict_size = len(self.__data)
        self.sentence_count = sum(word.as_first for word in self.__data.values())

    def learn(self, file):
        # translator = str.maketrans('', '', string.punctuation)
        translator = str.maketrans('', '', '\"\'@\\/()»«')
        ends = [
            '…',
            '...',
            '..',
            ';'
        ]

        with open(file, "r", encoding="utf8") as f:
            text = f.read().lower()

            for end in ends:
                text = text.replace(end, '.')
            sentences = tokenize.sent_tokenize(text)
            print("     done tokenize")
            for sentence in sentences:
                words = sentence.translate(translator).split()
                if len(words) > self.prefix_size:
                    last = words[-self.prefix_size:]
                    first = words[:self.prefix_size]
                    prev = first
                    for word in words[self.prefix_size:]:
                        # if all(char.isalpha() for char in (temp for temp in prev)):
                        #     if all(char.isalpha() for char in word):
                        if h(prev) not in self.__data:
                            self.__data[h(prev)] = self.Word(prev)
                        self.__data[h(prev)].count += 1
                        self.__data[h(prev)].add(word)
                        prev = prev[1:]
                        prev.append(word)
                        self.word_count += 1

                    if h(first) in self.__data:
                        self.__data[h(first)].as_first += 1
                    if h(last) in self.__data:
                        self.__data[h(last)].as_last += 1

    def suggest_first(self):
        return list(random.choices(
            population=[word.prefix for word in self.__data.values()],
            weights=[word.as_first for word in self.__data.values()],
            k=5
        ))

    def find_first(self, words):
        prefixes = self.__data.values()
        words = list(map(compose(str.lower, str.strip), words))

        def has_words(prefix: MultiDictionary.Word):
            return all([prefix.clean.count(word) > 0 for word in words])

        prefixes = list(filter(has_words, prefixes))

        return list(random.choices(
            population=[word.prefix for word in prefixes],
            weights=[(word.as_first / 2) + 2 for word in prefixes],
            k=min(len(prefixes), 5)
        ))

    def suggest_next(self):
        if h(self.current) not in self.__data or len(self.__data[h(self.current)].next) == 0:
            return {}
        return set(random.choices(
            population=list(self.__data[h(self.current)].next.keys()),
            weights=self.__data[h(self.current)].next.values(),
            k=5
        ))

    def select(self, word):
        self.current.append(word)
        if len(self.current) > self.prefix_size:
            self.current.pop(0)

    def select_all(self, text):
        for word in text:
            self.select(word)

    def next(self):
        return self.__data[h(self.current)].next if h(self.current) in self.__data else {}

    def count(self):
        return self.__data[h(self.current)].count if h(self.current) in self.__data else 0

    def as_first(self):
        return self.__data[h(self.current)].as_first if h(self.current) in self.__data else 0

    def as_last(self):
        return self.__data[h(self.current)].as_last if h(self.current) in self.__data else 0

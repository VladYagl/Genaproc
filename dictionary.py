import random
import string

from typing import Dict
from nltk import tokenize


# TODO: keep original capitalisation
# TODO private
class Dictionary:
    class Word:
        def __init__(self, text):
            self.text = text
            self.next = {}
            self.count = 0
            self.as_first = 0
            self.as_last = 0

        def __str__(self):
            return "str " + self.__repr__()

        def __repr__(self):
            return self.text  # + " #" + str(self.count) # + " -> " + str(self.next)

        def __lt__(self, other):
            return (self.as_first, self.count) < (other.as_first, other.count)

        def add(self, word):
            if word not in self.next:
                self.next[word] = 0
            self.next[word] += 1

    def __init__(self, file):
        self.__data: Dict[str, Dictionary.Word] = {}
        self.word_count = 0
        self.learn(file)
        self.dict_size = len(self.__data)
        self.sentence_count = sum(word.as_first for word in self.__data.values())

    def learn(self, file):
        translator = str.maketrans('', '', string.punctuation)

        with open(file, "r", encoding="utf8") as f:
            text = f.read().lower()

            # learn by sentences
            print("learn by sentences")
            sentences = tokenize.sent_tokenize(text)
            print("     done tokenize")
            for sentence in sentences:
                words = sentence.translate(translator).split()
                if len(words) > 0:
                    last = words[-1]
                    first = words.pop(0)
                    prev = first
                    for word in words:
                        if all(char.isalpha() for char in prev):
                            if all(char.isalpha() for char in word):
                                if prev not in self.__data:
                                    self.__data[prev] = self.Word(prev)
                                if word not in self.__data:
                                    self.__data[word] = self.Word(word)
                                self.__data[prev].count += 1
                                self.__data[prev].add(word)
                                prev = word
                                self.word_count += 1

                    if first in self.__data:
                        self.__data[first].as_first += 1
                    if last in self.__data:
                        self.__data[last].as_last += 1

    def suggest_first(self):
        return set(random.choices(
            population=[word.text for word in self.__data.values()],
            weights=[word.as_first for word in self.__data.values()],
            k=5
        ))

    def suggest_next(self, word):
        if word not in self.__data or len(self.__data[word].next) == 0:
            return {}
        return set(random.choices(
            population=list(self.__data[word].next.keys()),
            weights=self.__data[word].next.values(),
            k=5
        ))

    def next(self, word):
        return self.__data[word].next if word in self.__data else {}

    def count(self, word):
        return self.__data[word].count if word in self.__data else 0

    def as_first(self, word):
        return self.__data[word].as_first if word in self.__data else 0

    def as_last(self, word):
        return self.__data[word].as_last if word in self.__data else 0

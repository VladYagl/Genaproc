from tkinter import ttk
from multi_dictionary import MultiDictionary

import tkinter
import random
import pickle

root = tkinter.Tk()
buttons = []
first_sentence = True
first_word = True


def filter_unicode(a):
    return ''.join(filter(lambda x: ord(x) in range(32767), a))


def add(a):
    text.configure(state="normal")
    a = filter_unicode(a)
    text.insert(tkinter.END, a)
    text.configure(state="disabled")


def select(selected_word):
    global first_word
    if not first_word:
        add(' ')
    first_word = False
    d.select(selected_word)
    add(selected_word)

    entry.destroy()
    for button in buttons:
        button.destroy()

    for word in d.suggest_next():
        button = ttk.Button(root, text=filter_unicode(word), command=lambda text=word: select(text))
        buttons.append(button)
        button.grid()


def new():
    global first_sentence, first_word, entry
    if not first_sentence:
        add(" ")
    first_sentence = False
    first_word = True

    for button in buttons:
        button.destroy()

    for first in d.suggest_first():
        text = ' '.join(first).capitalize()

        def call(selected=first):
            d.select_all(selected[:-1])
            add(' '.join(selected[:-1]).capitalize())
            add(' ')
            select(selected[-1])

        button = ttk.Button(root, text=filter_unicode(text), command=lambda text=first: call(text))
        buttons.append(button)
        button.grid()

    def find(_):
        for first in d.find_first(words.get().split()):
            text = ' '.join(first).capitalize()

            def call(selected=first):
                d.select_all(selected[:-1])
                add(' '.join(selected[:-1]).capitalize())
                add(' ')
                select(selected[-1])

            button = ttk.Button(root, text=filter_unicode(text), command=lambda text=first: call(text))
            buttons.append(button)
            button.grid()

    words = tkinter.StringVar()
    entry = ttk.Entry(root, textvariable=words)
    entry.bind('<Return>', find)
    entry.grid()


def full():
    global text, first_sentence, first_word
    first_sentence = False

    for button in buttons:
        button.destroy()

    if first_word:
        first = random.sample(d.suggest_first(), 1)[0]
        add(' '.join(first).capitalize())
        d.select_all(first)

    while True:
        if len(d.next()) == 0:
            break

        word = random.sample(d.suggest_next(), 1)[0]
        d.select(word)
        add(" " + word)

    new()


def main():
    global text, root

    root.destroy()
    root = tkinter.Tk()

    ttk.Button(root, text="Random sentence", command=full).grid()

    ttk.Label(root, text="text size: " + str(d.word_count) + " dict size:" + str(d.dict_size)).grid()

    text = tkinter.Text(root)
    text.configure(state="disabled")
    text.grid()

    ttk.Button(root, text="New sentence", command=new).grid()
    new()


def dump_file(file: str):
    return file + ".dict"


def load():
    global d
    with open(dump_file(file.get()), 'rb') as f:
        d = pickle.load(f)
    main()


def build():
    global d
    d = MultiDictionary(prefix_size.get(), file.get())
    with open(dump_file(file.get()), 'wb') as f:
        pickle.dump(d, f)
    main()


file = tkinter.StringVar()
file.set("texts/pasta_chan.txt")

prefix_size = tkinter.IntVar()
prefix_size.set(2)

ttk.Entry(root, textvariable=prefix_size).grid()
ttk.Entry(root, textvariable=file).grid()
ttk.Button(root, text="Build new", command=build).grid()
ttk.Button(root, text="Load", command=load).grid()

root.mainloop()

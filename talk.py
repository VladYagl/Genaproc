from tkinter import ttk
from threading import Thread
from pynput.keyboard import Key, Controller, Listener

import sys
import tkinter
import random
import pickle
import time
import numpy as np

from dictionary import Dictionary

keyboard = Controller()
root = tkinter.Tk()
buttons = []
first_sentence = True
first_word = True
sizes = []


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
    add(selected_word)

    for button in buttons:
        button.destroy()

    for word in d.suggest_next(selected_word.lower()):
        button = ttk.Button(root, text=filter_unicode(word), command=lambda text=word: select(text))
        buttons.append(button)
        button.grid()


def new():
    global first_sentence, first_word
    if not first_sentence:
        add(". ")
    first_sentence = False
    first_word = True

    for button in buttons:
        button.destroy()

    for word in d.suggest_first():
        word = word.title()
        button = ttk.Button(root, text=filter_unicode(word), command=lambda text=word: select(text))
        buttons.append(button)
        button.grid()


def random_text(max_words=30, stop_chance=0.6):
    text = ""
    word = random.sample(d.suggest_first(), 1)[0]
    text += word.title()

    words = 1
    while True:
        if len(d.next(word)) == 0:
            break

        words += 1
        word = random.sample(d.suggest_next(word), 1)[0]
        text += " " + word

        as_last = d.as_last(word) / d.count(word) if d.count(word) > 0 else 0
        as_last_enchanted = as_last ** (1 / 5)
        rand = random.random()
        words_weight = ((words / 23) ** 2) * as_last_enchanted
        rand_weight = (rand ** 2.5) * as_last_enchanted
        # print(rand_weight + words_weight, word, "rand:", rand, rand_weight,
        #       "words:", words, words_weight, "as_last:", as_last, as_last_enchanted)
        if rand_weight + words_weight > 0.6 or words > 30:
            # print(word, "rand:", rand, rand_weight,
            #       "words:", words, words_weight, "as_last:", as_last, as_last_enchanted)
            break
    # print()

    global sizes
    sizes.append(words)

    return text

# TODO: extract "hyperparameters" to some args
def full():
    global text, first_sentence
    first_sentence = False

    for button in buttons:
        button.destroy()

    add(random_text())

    new()

repeat = True

def auto():
    print("Start!")
    global repeat
    repeat = True

    def spam():
        global repeat
        while repeat:
            n = random.randrange(20, 120)
            # n = random.randrange(5, 10)
            for i in range(n):
                if repeat == False:
                    break
                sys.stdout.write("\r" + str(i) + " / " + str(n) + " | ")
                time.sleep(1)

            for i in range(random.randrange(2) + random.randrange(2) +
                    random.randrange(2) + random.randrange(2)):
                if repeat == False:
                    break
                print("lets' go:", repeat)
                text = random_text(max_words=15, stop_chance=0.75)
                text = filter_unicode(text)
                print(text)
                keyboard.press(Key.enter);
                keyboard.release(Key.enter);
                keyboard.type("/all " + text)
                keyboard.press(Key.enter);
                keyboard.release(Key.enter);
                time.sleep(2)

    spamt = Thread(target=spam)
    spamt.start()

    def on_press(key):
        global repeat
        if key == Key.f10:
            return False
        if key == Key.f7:
            repeat = False
            print("over")
        if key == Key.f8:
            repeat = True
            spamt = Thread(target=spam)
            spamt.start()
            print("new")

    def daddy():
        with Listener(on_press=on_press) as listener:
            listener.join()

    daddyt = Thread(target=daddy)
    daddyt.start()


def main():
    global text, root

    root.destroy()
    root = tkinter.Tk()

    ttk.Button(root, text="Random sentence", command=full).grid()
    ttk.Button(root, text="Automate", command=auto).grid()

    ttk.Label(root, text="text size: " + str(d.word_count) + " dict size:" + str(d.dict_size)).grid()

    text = tkinter.Text(root)
    text.configure(state="disabled")
    text.grid()

    ttk.Button(root, text="New sentence", command=new).grid()
    new()

    # # uncomment to test sentence length distribution
    # print("#" * 100)
    # for i in range(1000):
    #     if i % 10 == 0:
    #         print("-", end="")
    #     full()
    # print("average: %0.2f (+/- %0.2f)" % (np.array(sizes).mean(), np.array(sizes).std()))
    #
    # import matplotlib.pyplot as plt
    # plt.subplots()
    # plt.hist(sizes, bins=15)
    # print(np.histogram(sizes, bins=15))
    # plt.show()


def load():
    global d
    with open('dict_save', 'rb') as f:
        d = pickle.load(f)
    main()


def build():
    global d
    d = Dictionary("texts/league.txt")
    with open('dict_save', 'wb') as f:
        pickle.dump(d, f)
    main()


ttk.Button(root, text="Build new", command=build).place(relx=.4, rely=.2)
ttk.Button(root, text="Load", command=load).place(relx=.4, rely=.5)

root.title("Genaproc")
root.geometry("400x80")
root.mainloop()

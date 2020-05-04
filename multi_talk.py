from tkinter import ttk
from multi_dictionary import MultiDictionary
from threading import Thread
from pynput.keyboard import Key, Controller, Listener
from functional import partial

import time
import os
import sys
import tkinter
import random
import pickle

keyboard = Controller()
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
        button = ttk.Button(
            root,
            text=filter_unicode(word),
            command=lambda text=word: select(text)
        )
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

        button = ttk.Button(
            root,
            text=filter_unicode(text),
            command=lambda text=first: call(text)
        )
        buttons.append(button)
        button.grid()

    search_buttons = []

    def find(_):
        for button in search_buttons:
            button.destroy()

        try:
            for first in d.find_first(words.get().split()):
                text = ' '.join(first).capitalize()

                def call(selected=first):
                    d.select_all(selected[:-1])
                    add(' '.join(selected[:-1]).capitalize())
                    add(' ')
                    select(selected[-1])

                button = ttk.Button(
                    root,
                    text=filter_unicode(text),
                    command=lambda text=first: call(text)
                )
                buttons.append(button)
                search_buttons.append(button)
                button.grid()
        except BaseException:
            label = ttk.Label(
                root,
                text="No sentese found starting with this word"
            )
            buttons.append(label)
            search_buttons.append(label)
            label.grid()

    words = tkinter.StringVar()
    entry = ttk.Entry(root, textvariable=words)
    entry.bind('<Return>', find)
    buttons.append(entry)
    entry.grid()


def random_text():
    text = ""
    first = random.sample(d.suggest_first(), 1)[0]
    text += ' '.join(first).capitalize()
    d.select_all(first)

    while True:
        if len(d.next()) == 0:
            break

        word = random.sample(d.suggest_next(), 1)[0]
        d.select(word)
        text += " " + word

    return text


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


def spam_text():
    global pls_stop
    text = random_text()
    text = filter_unicode(text)
    text = chat_prefix.get() + text
    print(text)

    keyboard.release(Key.shift)

    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    chance = 0.0
    for word in text.split(' '):
        if pls_stop:
            break
        chance += split_chance.get()
        keyboard.type(word + ' ')
        time.sleep(chat_delay.get() * len(word))
        if random.random() < chance:
            chance = 0.0
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            keyboard.press(Key.enter)
            time.sleep(0.03)
            keyboard.release(Key.enter)
            keyboard.type(chat_prefix.get())

    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    pls_stop = False


repeat = True
pls_stop = False


def auto():
    print("Start!")
    global repeat
    repeat = True

    def spam():
        delay = 50
        global repeat
        while repeat:
            n = random.randrange(10 + int(delay / 2), 60 + delay)
            # n = random.randrange(5, 10)
            for i in range(n):
                if not repeat:
                    break
                sys.stdout.write("\r" + str(i) + " / " + str(n) + " | ")
                time.sleep(1)

            if not repeat:
                break

            spam_text()

    def on_press(key):
        global repeat, pls_stop
        if key == settings.binds[spam_key]:
            singlet = Thread(target=spam_text)
            singlet.start()
        if key == settings.binds[kill_key]:
            pls_stop = True
        if key == settings.binds[stop_key]:
            repeat = False
            print("over")
        if key == settings.binds[start_key]:
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

    # ttk.Button(root, text="Automate", command=auto).grid()
    auto()

    ttk.Button(root, text="Random sentence", command=full).grid()

    ttk.Label(
        root,
        text="text size: " + str(d.word_count)
        + " dict size:" + str(d.dict_size)
    ).grid()

    text = tkinter.Text(root, height=10, width=40)
    text.configure(state="disabled")
    text.grid()

    ttk.Button(root, text="New sentence", command=new).grid()
    new()


def dump_file(file: str):
    return file + ".dict"


def save_settings():
    settings.file = file.get()
    settings.prefix_size = prefix_size.get()
    settings.chat_prefix = chat_prefix.get()
    settings.split_chance = split_chance.get()
    settings.chat_delay = chat_delay.get()

    with open(settings_file, 'wb') as f:
        pickle.dump(settings, f)


def load():
    global d
    save_settings()
    with open(dump_file(file.get()), 'rb') as f:
        d = pickle.load(f)
    main()


def build():
    global d
    save_settings()
    d = MultiDictionary(prefix_size.get(), file.get())
    with open(dump_file(file.get()), 'wb') as f:
        pickle.dump(d, f)
    main()


def pick():
    filename = tkinter.filedialog.askopenfilename(initialdir=os.getcwd())
    file.set(filename)


start_key = 0
stop_key = 1
spam_key = 2
kill_key = 3

texts = [
        None, None, None, None
    # ttk.Label(root, text=""),
    # ttk.Label(root, text=""),
    # ttk.Label(root, text=""),
    # ttk.Label(root, text="")
]

names = [
    "Start",
    "Stop",
    "Spam",
    "Kill"
]


def update_binds():
    print("start")
    for i in range(4):
        if texts[i] == None:
            texts[i] = ttk.Label(root, text="")
        print(i, names[i], settings.binds[i])
        texts[i].configure(text=f"{names[i]} key: {settings.binds[i]}")


def show_settings():

    def bind(bind_key):
        print(f"binding : {bind_key}")

        def press(key):
            settings.binds[bind_key] = key
            print(f"bind_key = {bind_key} | new_key = {key}")
            listener.stop()

        with Listener(on_press=press) as listener:
            listener.join()
            update_binds()

    ttk.Label(root).grid(columnspan=2)
    frame = tkinter.Frame()
    frame.grid(columnspan=2)

    ttk.Label(root, text="----------Settings----------").grid(
        columnspan=2, in_=frame
    )
    label = ttk.Label(root, text="Chat Prefix")
    label.grid(sticky=tkinter.E, in_=frame)
    ttk.Entry(root, textvariable=chat_prefix).grid(
        column=1, row=label.grid_info()['row'], sticky=tkinter.W, in_=frame
    )
    label = ttk.Label(root, text="Number of words")
    label.grid(sticky=tkinter.E, in_=frame)
    ttk.Entry(root, textvariable=prefix_size).grid(
        column=1, row=label.grid_info()['row'], sticky=tkinter.W, in_=frame
    )
    label = ttk.Label(root, text="Split chance")
    label.grid(sticky=tkinter.E, in_=frame)
    ttk.Entry(root, textvariable=split_chance).grid(
        column=1, row=label.grid_info()['row'], sticky=tkinter.W, in_=frame
    )
    label = ttk.Label(root, text="Chat delay")
    label.grid(sticky=tkinter.E, in_=frame)
    ttk.Entry(root, textvariable=chat_delay).grid(
        column=1, row=label.grid_info()['row'], sticky=tkinter.W, in_=frame
    )

    update_binds()

    for i in range(4):
        texts[i].grid(sticky=tkinter.E, in_=frame)
        ttk.Button(
            root,
            text="Bind",
            command=partial(bind, i)
        ).grid(sticky=tkinter.W, column=1, row=texts[i].grid_info()['row'], in_=frame)


class Settings:
    def __init__(self):
        self.file = "texts/league.txt"
        self.prefix_size = 2
        self.chat_prefix = "/all "
        self.split_chance = 0.03
        self.chat_delay = .05
        self.binds = [
            Key.f8,
            Key.f7,
            Key.f9,
            Key.f10
        ]


settings_file = 'settings.cum'

try:
    with open(settings_file, 'rb') as f:
        settings = pickle.load(f)
except BaseException as e:
    print(e)
    settings = Settings()

file = tkinter.StringVar()
file.set(settings.file)
prefix_size = tkinter.IntVar()
prefix_size.set(settings.prefix_size)
chat_prefix = tkinter.StringVar()
chat_prefix.set(settings.chat_prefix)
split_chance = tkinter.DoubleVar()
split_chance.set(settings.split_chance)
chat_delay = tkinter.DoubleVar()
chat_delay.set(settings.chat_delay)

frame = ttk.Frame()
frame.grid(columnspan=2)
ttk.Entry(root, textvariable=file, width=40).grid(in_=frame)
ttk.Button(root, text="Select file", command=pick).grid(column=1, row=0, in_=frame)
btn = ttk.Button(root, text="Build new", command=build)
btn.grid(sticky=tkinter.E)
ttk.Button(root, text="Load", command=load).grid(
    row=btn.grid_info()['row'], column=1, sticky=tkinter.W
)

show_settings()

root.mainloop()

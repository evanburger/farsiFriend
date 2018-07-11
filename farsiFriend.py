#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Farsi Friend
Created on Mon Jul  2 16:45:31 2018

@author: Evan Mildenberger
"""


__version__ = "v0.3.2"


import random
import logging


# set up logging
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)-12s - %(levelname)-8s - %(message)s")

# dataset for vocabulary. format is list of (English, Persian script, Persian pronunciaion) tuples
vocab = [("water", "آب", "aab"),
         ("dog", "سگ", "sag"),
         ("life", "زندگی", "zendegi"),
         ("man", "مرد", "mard"),
         ("working", "کر کردن", "kaar kardan")]

# define functions
def getWords(vocab):
    """Return a randomly chosen tuple given a list of tuples.
    getWords(list) --> tuple
    """
    logging.info("getWords started")
    # select random word tuple from vocab list
    words = vocab[random.randrange(len(vocab))]
    logging.info("getWords ended")
    return words

def getSpecWord(words):
    """Return a randomly chosen string given tuple of strings.
    getSpecWord(tuple) --> string
    """
    logging.info("getSpecWord started")
    index = random.randrange(2) # randomly select 0 or 1
    logging.info("getSpecWord ended")
    return index, words[index]

def getInput(index, word):
    """Print given string, then return string received as input.
    getInput(string) --> string
    """
    logging.info("getInput started")
    if index == 0:
        language = "Finglish"
    else:
        language = "English"
    logging.info("getInput ended")
    return input(f"What is the {language} translation of {word}? ")

def compareWords(userInput, actualWord):
    """Print string depending on given strings, return None.
    compareWords(string, string) --> None
    """
    logging.info("compareWords started")
    if userInput == actualWord:
        print("\nYou are correct!\n")
    else:
        print(f'\nSorry, that is wrong. It\'s actually "{actualWord}"\n')
    logging.info("compareWords ended")


# define main function
def main():
    logging.info("main loop started")
    words = getWords(vocab)
    logging.debug("words var: %s", words)
    index, word = getSpecWord(words)
    logging.debug("index, word vars: %s, %s", index, word)
    userInput = getInput(index, word)
    logging.debug("userInput var: %s", userInput)
    if userInput.lower() == "q":
        logging.info("farsiFriend.py exited")
        quit() # quit if user enters something like quit
    if index == 0:
        actualWord = words[2] # User to input Persian pron if given English word
    else:
        actualWord = words[0] # User to input English word if given Persian script
    logging.debug(f"actualWord var: %s", actualWord)
    compareWords(userInput, actualWord)
    logging.info("main loop ended")
    main()


# assertions
assert vocab, "vocab var is missing"

# print initial message, then call main function
if __name__ == "__main__":
    logging.info("farsiFriend.py started")
    print(
'''\nWelcome to FarsiFriend!
Enter the respective translations to the prompts to see if you're correct.
Enter 'q' to exit.
    ''')
    main()
else:
    logging.warning("this file is not intended to be imported")
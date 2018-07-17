#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Farsi Friend
Created on Mon Jul  2 16:45:31 2018

@author: Evan Mildenberger
"""

# ==============================================================================
# NOTES
# BUG - If IndexError thrown even once, the vocab.pop(randNumber) line
# in getWords always returns a NoneType even if during that iteration of main
# the randNumber is within the index range of the vocab list. Turning that line off
# and setting randNumber to a constant number fixes the bug. The bug is also
# fixed by calling main in the except block of getWords
# ==============================================================================


__version__ = "v0.4.0"


import random
import logging


#  set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

fileHandler = logging.FileHandler("farsiFriend.log")
fileHandler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)-12s - %(levelname)-8s - %(message)s")
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)
streamHandler.setLevel(logging.DEBUG)
logger.addHandler(streamHandler)

#  dataset for vocabulary. format is list of
#  (English, Persian script, Persian pronunciaion) tuples
vocab = [("water", "آب", "aab"),
         ("dog", "سگ", "sag"),
         ("life", "زندگی", "zendegi"),
         ("man", "مرد", "mard"),
         ("working", "کار کردن", "kaar kardan"),
         ("sanctifying", "تقدیس کردن", "moqadis kardan"),
         ("accusation", "اتهام", "etehaam"),
         ("quality", "کیفیت", "kifit"),
         ("reputation", "شهرت", "shorat"),
         ("esteem", "احترام", None),
         ("endurance", "تحمل", None)]


#  define functions
def getWords(vocab):
    """Return a randomly chosen tuple that's popped from a given a list of tuples.
    getWords(list) --> tuple
    """
    logger.info("getWords started")
    #  select random word tuple from vocab list
    randNumber = random.expovariate(2 / len(vocab))
    logger.debug(f"randNumber : {randNumber}")
    # randNumber cannot exceed len(vocab) after conversion to int
    randNumber = int(round(randNumber))
    logger.debug(f"randNumber as int : {randNumber}")
    try:
        words = vocab.pop(randNumber)  # BUG - words var is None on second pass of program
        logger.info("getWords ended")
        return words
    except IndexError as err:
        logger.warning(err)
        main(vocab)


def getSpecWord(words):
    """Return a randomly chosen string given tuple of strings.
    getSpecWord(tuple) --> string
    """
    logger.info("getSpecWord started")
    index = random.randrange(2)  # randomly select 0 or 1
    logger.info("getSpecWord ended")
    return index, words[index]


def getInput(index, word):
    """Print given string, then return string received as input.
    getInput(string) --> string
    """
    logger.info("getInput started")
    if index == 0:
        language = "Finglish"
    else:
        language = "English"
    logger.info("getInput ended")
    userInput = input(f"What is the {language} translation of {word}? ")
    return userInput


def compareWords(userInput, actualWord, vocab, words):
    """Print string depending on given strings,
    return vocab with inserted tuple of strings.
    compareWords(string, string) --> list
    """
    logger.info("compareWords started")
    if userInput == actualWord:
        print("\nYou are correct!\n")
        #  append words to end of vocab to lower probabilty
        vocab.append(words)
        logger.info(f"words var {words} appended at end of vocab var")
    else:
        print(f'\nSorry, that is wrong. It\'s actually "{actualWord}"\n')
        #  insert words at beginning of vocab to increase probabilty
        vocab.insert(0, words)
        logger.info(f"words var {words} inserted at beginning of vocab var")
    logger.info("compareWords ended")
    return vocab


# define main function
def main(vocab):
    logger.info("main loop started")
    logger.debug(f"vocab var at start of main: {vocab}")
    words = getWords(vocab)
    logger.debug(f"words var: {words}")
    index, word = getSpecWord(words)
    logger.debug(f"index, word vars: {index}, {word}")
    userInput = getInput(index, word)
    logger.debug("userInput var: {userInput}")
    if userInput.lower() == "q":
        logger.info("farsiFriend.py exited")
        quit()  # quit if user enters something like quit
    if index == 0:
        #  User to input Persian pron if given English word
        actualWord = words[2]
    else:
        #  User to input English word if given Persian script
        actualWord = words[0]
    logger.debug(f"actualWord var: {actualWord}")
    vocab = compareWords(userInput, actualWord, vocab, words)
    logger.debug(f"vocab var at end of main: {vocab}")
    logger.info("main loop ended")
    main(vocab)


# print initial message, then call main function
if __name__ == "__main__":
    logger.info("farsiFriend.py started")
    print('''\nWelcome to FarsiFriend!
    Enter the respective translations to the prompts to see if you're correct.
    Enter 'q' to exit.
    ''')
    main(vocab)
else:
    logger.warning("This file is not intended to be imported")

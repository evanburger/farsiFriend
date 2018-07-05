#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Farsi Friend
Created on Mon Jul  2 16:45:31 2018

@author: Evan Mildenberger
"""

import random

__version__ = "v0.3.0"

# dataset for vocabulary. format is list of (English, Persian script, Persian pronunciaion) tuples
vocab = [("water", "آب", "aab"), ("dog", "سگ", "sag"), ("life", "زندگی", "zendegi"), ("man", "مرد", "mard"), ("working", "کر کردن", "kaar kardan")]

# define functions
def getWords(vocab):
    ''' getWords(list) --> tuple
    Return a randomly chosen tuple given a list of tuples
    '''
    return vocab[random.randrange(len(vocab))] # select random word tuple from vocab list

def getSpecWord(words):
    '''getSpecWord(tuple) --> string
    Return a randomly chosen string given tuple of strings
    '''
    index = random.randrange(2) # randomly select 0 or 1
    return index, words[index]

def getInput(index, word):
    '''getInput(string) --> string
    Print given string, then return string received as input
    '''
    if index == 0:
        language = "Finglish"
    else:
        language = "English"
    return input(f"What is the {language} translation of {word}? ")

def compareWords(userInput, actualWord):
    '''compareWords(string, string) --> None
    Print string depending on given strings, return None
    '''
    if userInput == actualWord:
        print("\nYou are correct!\n")
    else:
        print(f'\nSorry, that is wrong. It\'s actually "{actualWord}"\n')

# define main function
def main():
    words = getWords(vocab)
    index, word = getSpecWord(words)
    userInput = getInput(index, word)
    if userInput.lower()[0] == "q":
        quit() # quit if user enters something like quit
    if index == 0:
        actualWord = words[2] # User to input Persian pron if given English word
    else:
        actualWord = words[0] # User to input English word if given Persian script
    compareWords(userInput, actualWord)
    main()

# print initial message, then call main function
if __name__ == "__main__":
    print(
'''\nWelcome to FarsiFriend!
Enter the respective translations to the prompts to see if you're correct.
Enter 'quit' to exit.
    ''')
    main()
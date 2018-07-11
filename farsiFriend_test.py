#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 12:45:16 2018

@author: evan
"""

import random
import unittest
from unittest.mock import patch # for mocking purposeses

from farsiFriend import *


#def getWords(vocab):
#    ''' getWords(list) --> tuple
#    Return a randomly chosen tuple given a list of tuples
#    '''
#    return vocab[random.randrange(len(vocab))] # select random word tuple from vocab list
#
#def getSpecWord(words):
#    '''getSpecWord(tuple) --> string
#    Return a randomly chosen string given tuple of strings
#    '''
#    index = random.randrange(2) # randomly select 0 or 1
#    return index, words[index]
#
#def getInput(index, word):
#    '''getInput(string) --> string
#    Print given string, then return string received as input
#    '''
#    if index == 0:
#        language = "Finglish"
#    else:
#        language = "English"
#    return input(f"What is the {language} translation of {word}? ")
#
#def compareWords(userInput, actualWord):
#    '''compareWords(string, string) --> None
#    Print string depending on given strings, return None
#    '''
#    if userInput == actualWord:
#        print("\nYou are correct!\n")
#    else:
#        print(f'\nSorry, that is wrong. It\'s actually "{actualWord}"\n')


class Test(unittest.TestCase):
    
    def test_getWords_argument_good(self):
        self.assertIsInstance(getWords(vocab), tuple) # test that tuple is returned
        self.assertEqual(len(getWords(vocab)), 3) # test that tuple has 3 elements
        for word in getWords(vocab):
            self.assertIsInstance(word, str) # test that each element in tuple is a string
    
    def test_getSpecWord(self):
        self.assertEqual(len(getSpecWord(("water", "آب", "aab"))), 2) # test that function returns tuple of 2 elements
        self.assertIsInstance(getSpecWord(("water", "آب", "aab"))[0], int) # test that first element returned is int
        self.assertIsInstance(getSpecWord(("water", "آب", "aab"))[1], str) # test that second element returned is str
        
    def test_getInput(self):
        pass
    
    def test_compareWords(self):
        pass
        

if __name__ == "__main__":
    unittest.main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 12:45:16 2018

@author: evan
"""


# =============================================================================
# TO DO
#
# =============================================================================


import random
import unittest

from farsiFriend import getWords, getSpecWord, getInput, compareWords, vocab


class Test(unittest.TestCase):

    def setUp(self):
        self.vocab = vocab
        self.words = ("water", "آب", "aab")

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_getWords_argument_good(self):
        #  test that tuple is returned
        self.assertIsInstance(getWords(self.vocab), tuple)
        #  test that tuple has 3 elements
        self.assertEqual(len(getWords(self.vocab)), 3)
        for word in getWords(self.vocab):
            #  test that each element in tuple is a string
            self.assertIsInstance(word, str)

    def test_getSpecWord(self):
        # test that function returns tuple of 2 elements
        self.assertEqual(len(getSpecWord(self.words)), 2)
        # test that first element returned is int
        self.assertIsInstance(getSpecWord(self.words)[0], int)
        # test that second element returned is str
        self.assertIsInstance(getSpecWord(self.words)[1], str)

    def test_getInput(self):
        pass

    def test_compareWords(self):
        pass


if __name__ == "__main__":
    unittest.main()

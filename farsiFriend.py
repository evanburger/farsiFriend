#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Farsi Friend
Created on Mon Jul  2 16:45:31 2018

@author: Evan Mildenberger
"""

# ==============================================================================
# TO DO
# Hide passwords upon entry
# Hash salted passwords for user accounts
# state what type of word it is to help disambiguate
# ==============================================================================


__version__ = "0.6.0"


import random
import logging
import getpass

import pymysql as sql
import passlib.hash

import sensitiveData


DB = "FarsiFriend"


#  set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

fileHandler = logging.FileHandler("./logs/farsiFriend.log")
fileHandler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)-12s - %(levelname)-8s - %(message)s")
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)
streamHandler.setLevel(logging.WARNING)
logger.addHandler(streamHandler)


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
        words = vocab.pop(randNumber)
        logger.info("getWords ended")
        return words
    except IndexError as err:
        logger.warning(err)
        loggedIn = True
        main(loggedIn)


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
        print(f'\nSorry, that is wrong. It\'s actually "{actualWord}" ({words[1]}).\n')
        #  insert words at beginning of vocab to increase probabilty
        vocab.insert(0, words)
        logger.info(f"words var {words} inserted at beginning of vocab var")
    logger.info("compareWords ended")
    return vocab

def logIn():
    
    logger.info("logIn started")
    conn = sql.connect(db=DB, user=sensitiveData.USER, password=sensitiveData.PASSWORD)
    c = conn.cursor()

    username = input("Enter your username: ")
    logger.debug(f"username = {username}")
    if username.lower() == 'q':
        quit()
    c.execute("SELECT username FROM users WHERE username = %s;", (username,))
    logger.info("SELECT query executed")
    while c.fetchone() is None:
        username = input("No such username exists. Try again: ")
        logger.debug(f"username = {username}")
        if username.lower() == 'q':
            quit()
        c.execute("SELECT username FROM users WHERE username = %s;", (username,))
        logger.info("SELECT query executed")

    userPassword = getpass.getpass("Enter your password (will not appear on screen): ")
    if userPassword.lower() == "q":
        del userPassword
        quit()
    c.execute("SELECT password FROM users WHERE username = %s;", (username,))
    logger.info("SELECT query executed")
    while not passlib.hash.sha256_crypt.verify(userPassword, c.fetchone()[0]):
        userPassword = getpass.getpass("Password is incorrect. Try again: ")
        if userPassword.lower() == "q":
            del userPassword
            quit()
        c.execute("SELECT password FROM users WHERE username = %s;", (username,))
        logger.info("SELECT query executed")

    #  This point is only reached if the username entered exists in the DB and the password entered matches the DB's one.
    userID = c.execute("SELECT user_ID FROM users WHERE username = %s;", (username,))
    conn.close()
    logger.info("logIn ended")
    return userID

def loadVocab(userID):
    
    logger.info("loadVocab started")
    conn = sql.connect(db = DB, user=sensitiveData.USER, password=sensitiveData.PASSWORD)
    c = conn.cursor()
    
    #  The user_words table must be wipped to allow for a refresh of words that the user knows.
    c.execute("DELETE FROM user_words WHERE user_ID = %s;", (userID,))
    c.execute("INSERT INTO user_words SELECT NULL, %s, word_ID FROM words;", (userID,))

    c.execute("SELECT word_ID FROM user_words WHERE user_ID = %s;", (userID,))
    logger.info("SELECT query executed")
    wordIDList = c.fetchall()
    logger.debug(f"wordIDList = {wordIDList}")

    vocab = []
    for wordID in wordIDList:
        c.execute("SELECT english, persian, finglish, word_ID FROM words WHERE word_ID = %s;", (wordID))
    #  Vocab must be made into a list of tuples to allow reordering later on.
        vocab.append(c.fetchone())
    logger.debug(f"vocab = {vocab}")

    conn.close()
    logger.info("loadVocab ended")
    return vocab

def register():
    
    logger.info("register started")
    conn = sql.connect(db = DB, user=sensitiveData.USER, password=sensitiveData.PASSWORD)
    c = conn.cursor()

    username = input("Enter a username (up to 32 characters): ")
    logger.debug(f"username = {username}")
    if username.lower() == 'q':
        quit()
    password = getpass.getpass("Enter a password [up to 32 characters] (will not appear on screen): ")
    if password.lower() == "q":
        del password
        quit()
    
    confirmedPassword = getpass.getpass("Enter password again to confirm: ")
    if confirmedPassword.lower() == "q":
        del confirmedPassword
        quit()
    
    if password != confirmedPassword:
        print("Passwords don't match. Try again.")
        conn.close()
        register()

    password = passlib.hash.sha256_crypt.encrypt(password)
    logger.debug(f"password = {password}")

    c.execute("INSERT INTO users VALUES (NULL, %s, %s);", (username, password))
    logger.info("Insert query executed")
    conn.commit()
    conn.close()
    logger.info("register ended")

def quitApp(userID, words):
    if userID == 1:
        quit()
    else: #  This is to save the state of the user's session to the DB.
        conn = sql.connect(db=DB, user=sensitiveData.USER, password=sensitiveData.PASSWORD)
        c = conn.cursor()
        c.execute("DELETE FROM user_words WHERE user_ID = %s;", (userID,))
        logger.info("DELETE query executed")
        for words in vocab:
            c.execute("INSERT INTO user_words VALUES (NULL, %s, %s);", (userID, words[3]))
        logger.info("INSERT queries executed")
        conn.commit()
        conn.close()
        logger.info("farsiFriend.py exited")
        quit()

# define main function
def main(loggedIn):
    
    if not loggedIn:
        while True: #  This block loops unitl q, l or r is entered.
            userLoggingIn = input("Log in or register? (l / r): ")
            if userLoggingIn.lower() == 'q':
                quit()
            elif userLoggingIn.lower() == 'l':
                break
            elif userLoggingIn.lower() == 'r':
                register()
                break

        global userID
        userID = logIn()
        global vocab
        vocab = loadVocab(userID)

    else:
        logger.info("main loop started")
        words = getWords(vocab)
        logger.debug(f"words var: {words}")
        index, word = getSpecWord(words)
        logger.debug(f"index, word vars: {index}, {word}")
        userInput = getInput(index, word)
        logger.debug(f"userInput var: {userInput}")
        if userInput.lower() == "q":
            quitApp(userID, words)
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
        
    loggedIn = True
    main(loggedIn)


# print initial message, then call main function
if __name__ == "__main__":
    logger.info("farsiFriend.py started")
    print('''\nWelcome to FarsiFriend!
    Enter the respective translations to the prompts to see if you're correct.
    Enter 'q' to exit.
    ''')
    loggedIn = False
    main(loggedIn)
else:
    logger.warning("This file is not intended to be imported")

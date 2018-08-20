#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update Vocab
This is a program designed to easily add words to the database storing vocabulary for Farsi Friend.
Created on Mon Aug 12 21:53:00 2018

@author: Evan Mildenberger
"""

# ==============================================================================
# NOTES
# 
# TO DO
# 
# ==============================================================================


__version__ = "0.3.1"


import logging
import sys
import os
from datetime import datetime
import getpass

import pymysql as sql


DB = 'PersianVocabulary'
USER = 'root'

fileMode = False


#  The fileHandler writes info and above to a file while the streamHandler writes to the console.
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logFilePath = f"./logs/updateVocab_{str(datetime.now())}.log"
os.makedirs(os.path.dirname(logFilePath), exist_ok=True) #  This makes a logs directory if there isn't one.
fileHandler = logging.FileHandler(logFilePath)
fileHandler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)-12s - %(levelname)-8s - %(message)s")
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)

#  These sys arguments set the logging level.
try:
    if (sys.argv[1] == "--debug" or sys.argv[1] == "-d"):
        streamHandler.setLevel(logging.DEBUG)
    elif (sys.argv[1] == "--full" or sys.argv[1] == "-f"):
        streamHandler.setLevel(logging.CRITICAL)
    elif (sys.argv[1] == "--bulk" or sys.argv[1] == "-b"):
        #  This is to avoid having the logger show all debugging info when in bulk entry mode.
        streamHandler.setLevel(logging.INFO)    
except IndexError: #  This exception occurs when no sys arguments are given.
    streamHandler.setLevel(logging.INFO)

logger.addHandler(streamHandler)


class InputTypeError(TypeError):
    """This error is to be raised when input made by the user doesn't meet the requirements of the program."""


def consolidateWords(userList, fileMode):
    #  Check to see if there are compound verbs.
    logger.debug("consolidateWords started")
    try:
        if len(userList) == 4: #  This is the usual case, so no action is required.
            logger.info("userList length = 4")
        elif len(userList) == 5: #  This occurs when two English words translate to one Persian word.
            logger.info("userList length = 4")
            userList = [f"{userList[0]} {userList[1]}", userList[2], userList[3], userList[4]]
        elif len(userList) == 6: #  This occurs when one English word translates to two words in Persian.
            logger.info("userList length = 4")
            userList = [userList[0], f"{userList[1]} {userList[2]}", f"{userList[3]} {userList[4]}", userList[5]]
        elif len(userList) == 7: #  This occurs when two English words translate to two words in Persian.
            logger.info("userList length = 4")
            userList = [f"{userList[0]} {userList[1]}", f"{userList[2]} {userList[3]}", f"{userList[4]} {userList[5]}", userList[6]]
        else:
            raise InputTypeError
    except InputTypeError as error:
        logger.error(error)
        logger.error(f"InputTypeError: only {len(userList)} words entered, 4, 6 or 7 expected")
        if fileMode:
            quit()
        else:
            getInput()
    logger.debug("consolidateWords ended")
    return userList

def updateVocabFromFile(filePath):
    print("""
Update Vocab --File Mode--
This program is an interface to add entries into the PersianVocabulary database.
""")
    with open(filePath) as file:
        data = []
        fileMode = True
        for line in file:
            userList = line.strip("\n").lower().split(" ")
            userList = consolidateWords(userList, fileMode)
            data = storeInput(data, userList)
            logger.info(f"data = {data}")
        updateVocab(data, DB, USER, fileMode)

def storeInputFromFile():
    filePath = input("Enter the file path of the text file to enter: ")
    with open(filePath) as file:
        data = []
        for line in file:
            userList = line.strip("\n").lower().split(" ")
            logger.info(f"userList = {userList}")
            data = storeInput(data, userList)
        logger.info(f"data = {data}")
    return data

def getInput():

    logger.debug("getInput started")
    userInput = input("Enter English, Finglish, Persian, and type seperated by a space: ").lower()

    if userInput == 'q':
        print("Update Vocab exited")
        quit()
    elif userInput == "":
        userList, repeat = None, False
        logger.info(f"repeat = {repeat}")
        return (userList, repeat)
    userList = userInput.split(" ")
    logger.info(f"userList = {userList}")

    fileMode = False
    userList = consolidateWords(userList, fileMode)
    logger.info(f"userList = {userLIst}")

    logger.debug("getInput ended")
    repeat = True
    logger.info(f"repeat = {repeat}")
    return (userList, repeat)

def storeInput(data, userList):
    logger.debug("storeInput started")
    data.append(tuple(userList))
    logger.debug("storeInput ended")
    return data

def getPassword():
    logger.debug("getPassword started")
    password = getpass.getpass("Enter the password for the database (will not appear on screen): ")
    logger.debug("getPassword ended")
    return password

def updateVocab(data, DB, USER, fileMode):

    logger.debug("updateVocab started")
    password = getPassword()
    conn = sql.connect(db=DB, user=USER, password=password)
    del password
    c = conn.cursor()

    queries = []
    for datum in data:
        logger.info(f"datum = {datum}")
        queries.append("INSERT INTO words VALUES (%s, %s, %s, %s, NULL);")
        logger.info(f"queries = {queries}")
    for query, datum in zip(queries, data):
        c.execute(query, datum) #  Inputs are sanitized
        logger.debug("query executed")

    conn.commit()
    conn.close()
    logger.debug("updateVocab ended")
    if fileMode:
        print("Update successful.")
        quit()


def main(fileMode):

    logger.debug("main started")

    if fileMode: #  This occurs when --bulk or -b are given as a sys argument.
        logger.info(f"fileMode = {fileMode}")
        print("""
Update Vocab --File Mode--
This program is an interface to add entries into the PersianVocabulary database.
""")
        data = storeInputFromFile()
        updateVocab(data, DB, USER, fileMode)

    elif not fileMode:
        logger.info(f"fileMode = {fileMode}")
        print("""
Update Vocab
This program is an interface to add entries into the PersianVocabulary database.

Enter words as directed. Press enter with nothing entred to save the words. Enter q to exit.
""")
        userList, repeat = getInput()
    
        data = []

        while repeat:
            data = storeInput(data, userList)
            logger.info(f"data = {data}")
            userList, repeat = getInput()

    updateVocab(data, DB, USER, fileMode)

    print("Update successful.")


#  These optional sys arguments show either available options or allow the input of file contents.
try:
    if (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
        print("""python updateVocab.py [-h | -d | -f]
    Optional arguments:
    --help, -h      Display optional arguments
    --debug, -d     Run program with all logging displayed
    --full, -f      Run program with only errors displayed""")
        quit()

    elif (sys.argv[1] == "--bulk" or sys.argv[1] == "-b"):
        try:
            updateVocabFromFile(sys.argv[2])
        except IndexError: #  This occurs when no file name is provided as a sys argument.
            fileMode = True #  The control flow continues to main
except IndexError: #  This exception occurs when no sys arguments are given.
    pass


if __name__ == "__main__":
    main(fileMode)


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
# make all inputs lowercase before adding to lists in order to allow for mixed case user inputs
# allow for more than 4 word inputs
# ==============================================================================


__version__ = "0.2.0"


import logging
import sys

import pymysql as sql


DB = 'PersianVocabulary'
USER = 'root'

#  The set logging level is based on sys arguments. There's also an argument for help.
if (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
    print("""python updateVocab.py [-h | -d | -f]
Optional arguments:
--help, -h      Display optional arguments
--debug, -d     Run program with all logging displayed
--full, -f      Run program with only errors displayed""")
    quit()

elif (sys.argv[1] == "--debug" or sys.argv[1] == "-d"):
    logging.basicConfig(level=logging.DEBUG)
elif (sys.argv[1] == "--full" or sys.argv[1] == "-f"):
    logging.basicConfig(level=logging.ERROR)

def getInput():
    logging.debug("getInput started")
    userInput = input("Enter English, Finglish, Persian, and type seperated by a space: ")
    logging.debug("getInput ended")
    return userInput

def storeInput(data, userList):
    logging.debug("storeInput started")
    data.append(tuple(userList))
    logging.debug("storeInput ended")
    return data

def getPassword():
    logging.debug("getPassword started")
    password = input("Enter the password for the database: ")
    logging.debug("getPassword ended")
    return password

def updateVocab(data, DB, USER):

    logging.debug("updateVocab started")
    password = getPassword()
    conn = sql.connect(db=DB, user=USER, password=password)
    del password
    c = conn.cursor()

    queries = []
    for datum in data:
        logging.info(f"datum = {datum}")
        queries.append("INSERT INTO words VALUES (%s, %s, %s, %s, NULL);")
        logging.info(f"queries = {queries}")
    for query, datum in zip(queries, data):
        logging.info(f"query = {query}")
        logging.info(f"datum = {datum}")
        c.execute(query, datum) #  Inputs are sanitized
        logging.debug("query executed")

    conn.commit()
    conn.close()
    logging.debug("updateVocab ended")


def main():

    logging.debug("main started")
    userInput = getInput()
    logging.info(f"userInput = {userInput}")
    if userInput == 'q':
        print("Update Vocab exited")
        quit()
    userList = userInput.split(" ")
    logging.info(f"userList = {userList}")
    data = []

    while userInput != "":
        data = storeInput(data, userList)
        logging.info(f"data = {data}")
        userInput = getInput()
        logging.info(f"userInput = {userInput}")
        if userInput == 'q':
            print("Update Vocab exited")
            quit()
        userList = userInput.split(" ")
        logging.info(f"userList = {userList}")
    updateVocab(data, DB, USER)

    print("""Update successful
Entries made:""")
    for line in data:
        print(line[0], line[1], line[2], line[3])


if __name__ == "__main__":
    main()


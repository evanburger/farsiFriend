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
# ==============================================================================


__version__ = "0.1.0"


import logging

import pymysql as sql


DB = 'PersianVocabulary'
USER = 'root'


logging.basicConfig(level=logging.DEBUG)


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


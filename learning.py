#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3 as lite
import sys
import math
import colorsys
import colorassociation

# Given a hue and a list of two colors, return the closer primirary hue
def bestMatch (twoColors, hue):
    if (abs(twoColors[0] - hue) < abs(twoColors[1] - hue)):
        return twoColors[0]
    else:
        return twoColors[1]

# Given a hue, return its name
def name (hue):
    if (hue >= 0 and hue < 60): return "Red"
    if (hue >= 60 and hue < 120): return "Yellow"
    if (hue >= 120 and hue < 180): return "Green"
    if (hue >= 180 and hue < 240): return "Cyan"
    if (hue >= 240 and hue < 300): return "Blue"
    if (hue >= 300 and hue < 360): return "Magenta"
    else: return "Red"

# Given a dList and name of a color, add it to the adjustment list
# of that color
def addToList (dList, nameColor):
    con = lite.connect('moo.db')
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO %s VALUES (%f, %f, %f, %f, %f, %f, %f)" % (nameColor, dList[0], dList[1], dList[2], dList[3], dList[4], dList[5], dList[6],))

# Given a hue, return its dList
def getDList (hue):
    con = lite.connect('moo.db')
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Colors WHERE Hue=%d" % hue)
        row = cur.fetchone()
        retlist = []
        for i in range (3, len(row)):
            retlist.append(row[i])
        return retlist

# Given a color's name, return its ID
def getID (hue):
    con = lite.connect('moo.db')
    with con:
        cur = con.cursor()
        cur.execute('SELECT * FROM Colors WHERE Hue=%d' % hue)
        row = cur.fetchone()
        return row[0]

# Given a hue, return its name
def getHue (nameColor):
    if nameColor == "Red": return 0.0
    if nameColor == "Yellow": return 60.0
    if nameColor == "Green": return 120.0
    if nameColor == "Cyan": return 180.0
    if nameColor == "Blue": return 240.0
    if nameColor == "Magenta": return 300.0

# Given a color's name, return amt. of votes
def getVotes (nameColor):
    con = lite.connect('moo.db')
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM %s" % nameColor)
        i = 0
        while cur.fetchone():
            i += 1
        return i

# Given an adjusted dList, update the color's main entry with that list
def putList (nameColor, dList):
    newupdated = []
    col = ["Dance", "Energy", "Tempo_Min", "Tempo_Max", "Mode", "Loud_Min", "Loud_Max"]
    for elem in dList:
        newupdated.append(elem)
    con = lite.connect('moo.db')
    with con:
        cur = con.cursor()
        i = 0
        for c in col:
            cur.execute('UPDATE Colors SET %s=%f WHERE Name="%s"' % (c, float(newupdated[i]), nameColor))
            i+=1
        
# Given a color's DList, the downvoted dList, and the name of its color,
# change the color's DList in respect to the downvote
def updateUp (colorDList, dList, nameColor):
    updated = []
    for elem in colorDList:
        updated.append(float(elem))
    for i in range (0, len(dList)):
        if i == 0 or i == 1 or i == 4:
            if (dList[i] > updated[i]):
                updated[i] += 0.01
            else:
                updated[i] -= 0.01
            if updated[i] > 1: updated[i] = 1
            if updated[i] < 0: updated[i] = 0
    putList (nameColor, updated)

   
# Given a color's DList, the downvoted dList, and the name of its color,
# change the color's DList in respect to the downvote
def updateDown (colorDList, dList, nameColor):
    updated = []
    for elem in colorDList:
        updated.append(elem)
        print (updated)
    for i in range (0, len(dList)):
        if i == 0 or i == 1 or i == 4:
            if (dList[i] > updated[i]):
                updated[i] -= 0.01
            elif (dList[i] < updated[i]):
                updated[i] += 0.01
            else: break
            if updated[i] > 1: updated[i] = 1
            if updated[i] < 0: updated[i] = 0
    putList (nameColor, updated)

# Given a hex value and a descriptor list, store the relevant descriptor list
# in the appropriate color-themed table in the 'moo.db' SQLite database
def thumbsUp (hex_in, dList):
    hue_in = colorassociation.hexToHue (hex_in)

    # Add the song's dList to the appropriate color's list.
    twoColors = colorassociation.between(hue_in)
    colorToAdd = bestMatch(twoColors, hue_in)
    nameColor = name (colorToAdd)
    addToList (dList, nameColor)
    colorDList = getDList (colorToAdd)
    updateUp (colorDList, dList, nameColor)


# Given a hex value and a descriptor list, store the relevant descriptor list
# in the appropriate color-themed table in the 'moo.db' SQLite database
def thumbsDown (hex_in, dList):
    hue_in = colorassociation.hexToHue (hex_in)

    # Add the song's dList to the appropriate color's list.
    twoColors = colorassociation.between(hue_in)
    colorToAdd = bestMatch(twoColors, hue_in)
    nameColor = name (colorToAdd)
    addToList (dList, nameColor)
    colorDList = getDList (colorToAdd)
    updateDown (colorDList, dList, nameColor)



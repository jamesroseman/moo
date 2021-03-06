#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

'''
Main SQLite structure:
    - Colors contains all colors and initial seeded values
    - Red/Yellow/etc. contains all up/downvoted song's descriptor lists
'''

con = lite.connect('moo.db')

colors = (
    (1, 'Red', 0, 0.5, 1, 0.5, 300, 0.5, -14, 0),
    (2, 'Yellow', 60, 1, 1, 100, 300, 0, -14, 0),
    (3, 'Green', 120, 1, 0.75, 100, 300, 0.5, -60, -14),
    (4, 'Cyan', 180, 1, 1, 100, 300, 0.5, -60, -14),
    (5, 'Blue', 240, 0.5, 0.5, 0, 120, 1, -60, -14),
    (6, 'Magenta', 300, 1, 0.75, 100, 300, 0.5, -14, 0)
)

colorlist = ["Red", "Yellow", "Green", "Cyan", "Blue", "Magenta"]

with con:

    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS Colors")
    cur.execute("CREATE TABLE Colors(Id INT, Name TEXT, Hue REAL, Dance REAL, \
                                 Energy REAL, Tempo_Min REAL, Tempo_Max REAL, \
                                     Mode REAL, Loud_Min REAL, Loud_Max REAL)")
    cur.executemany("INSERT INTO Colors VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",colors)

    for clr in colorlist:
        cur.execute ("DROP TABLE IF EXISTS %s" %clr)
        cur.execute("CREATE TABLE %s (Dance REAL, Energy REAL, Tempo_Min REAL, Tempo_Max REAL, Mode REAL, \
                                     Loud_Min REAL, Loud_Max REAL)" % clr)
    
    



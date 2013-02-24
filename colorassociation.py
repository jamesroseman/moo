#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3 as lite
import sys
import colorsys

# http://stackoverflow.com/questions/214359/converting-hex-color-to-rgb-and-vice-versa
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    if lv == 1:
        v = int(value, 16)*17
        return v, v, v
    if lv == 3:
        return tuple(int(value[i:i+1], 16)*17 for i in range(0, 3))
    return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))

# Returns list of (left_hue, right_hue) of the straddling hues of param
def between (color_hue):
    # Greater than Magenta causes problems
    if color_hue >= 300:
        return [300.0, 0.0]
    con = lite.connect('moo.db')
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Colors")
        while True:
            row = cur.fetchone()
            if row[2] == 0:
                left_hue = "Magenta"
            if row == None:
                break
            if row[2] > color_hue:
                return [left_hue, row[2]]
            left_hue = row[2]

# Get an attribute of a color given its hue
# e.g. getAttr (hue, "dance", 1, 3)
def getAttr (color_hue, loc):
    con = lite.connect('moo.db')
    with con:
        cur = con.cursor()
        req = ("SELECT * FROM Colors WHERE Hue=%d" % color_hue)
        cur.execute(req)
        con.commit()
        row = cur.fetchone()
        return float(row[loc])

# Evaluate proper input attribute value, given color_left, color_right
# multiplier, weight w, and location l
def evalAttr (attr, color_left, color_right, m, w, l):
    return float(w*((1-m)*getAttr(color_left, l) + m*getAttr(color_right, l)))


# Given a hex, return its hue
def hexToHue (hex_in):
    rgb = hex_to_rgb (hex_in)
    hsv = colorsys.rgb_to_hsv (rgb[0], rgb[1], rgb[2])
    return hsv[0] * 360

# Given a hex, return the list of descriptors which describe the color
# from the basis of danceability, energy, tempo, mode, and loudness
def hexToDescrip (hex_in):
    rgb = hex_to_rgb (hex_in)
    hsv = colorsys.rgb_to_hsv (rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0)

    hue = hsv[0] * 360
    sat = float(hsv[1]*100)
    bright = float(hsv[2]/255)*100
    print(hsv[0])
    print(hsv[1])
    print(hsv[2])

    color_left  = between(hue)[0]
    color_right = between(hue)[1]

    print(color_left)
    print(color_right)

    # Multiplier to average two attributes
    m = (hue % 60) / 60

    # Weights for saturation and brightness
    s = float(sat/100)
    b = float(bright/100)

    print(s)
    print(b)

    loc = []
    for i in range (0, 7):
        loc.append(i+3)
    attrs = ["Dance", "Energy", "Tempo_Min", "Tempo_Max", "Mode", "Loud_Min", "Loud_Max"]
    ws = [1, 1, 1, 1, 1, 1, 1]
    attval = []
    for i in range(0, len(attrs)):
        a = evalAttr(attrs[i], color_left, color_right, m, ws[i], loc[i])
        if (attrs[i] == "Dance" or attrs[i] == "Energy" or attrs[i] == "Loud_Min" or
            attrs[i] == "Loud_Max"):
            a *= (s * b)
        attval.append(a)
    return attval
    




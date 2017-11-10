#! /usr/bin/env python
#
# Support module generated by PAGE version 4.9
# In conjunction with Tcl version 8.6
#    Jul 08, 2017 04:54:16 PM


import sys
import tkMessageBox
import ast
from sharing import secret_int_to_points, points_to_secret_int

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1


def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top
    # initiate all the text field object
    #global shares, threshold, secret, splitText, combineText, splitAd, combineAd
    global shares, threshold, secret, splitText, combineText, splitAd
    shares = w.shareNum
    threshold = w.threshold
    secret = w.secret
    splitText = w.splitResult
    splitAd = w.splitAdvanceResult
    combineText = w.combineResult
    #combineAd = w.combineAdvanceResult

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

# display the msg on the text field
def displayTextField(textField, msg):
    textField.delete(1.0, END)
    textField.insert(INSERT, msg)

# convert string to integer. Open a message box if fails
def convertInt(s):
    try:
        return int(s)
    except Exception as e:
        tkMessageBox.showinfo( "Exception occurs", s + " is not an integer")
        print e
        
def split():
    # Check the input value as integer
    n = convertInt(shares.get())
    k = convertInt(threshold.get())
    S = convertInt(secret.get())
    # Calculate points
    (points, prime_num, coff) = secret_int_to_points(S, k, n)
    # Convert points to string
    msg = ""
    for point in points:
        msg = msg + str(point) + "\n"
    # display points
    displayTextField(splitText, msg)
    # display prime, coff
    displayTextField(splitAd, "p = " + str(prime_num) + "\n" + "Cofficient list = " + str(coff) + "\n")
    
def combine():
    # get all text from split text view
    temp = splitText.get(1.0, END)
    # form a list, each line is an element
    str_list = temp.split("\n")
    # remove the empty elements
    str_list = [x for x in str_list if x != '']
    # encode all elements to ascii
    points = []
    for str in str_list:
        points.append(ast.literal_eval(str.encode("ascii")))
    # calculate the secret
    sec = points_to_secret_int(points)
    # display the secret on the combine text view
    displayTextField(combineText, sec)

if __name__ == '__main__':
    import TSSDemo
    TSSDemo.vp_start_gui()
    
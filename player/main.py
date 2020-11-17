import sys
from ast import literal_eval
import time
import tkinter as tk


def q_key_pressed(event):
    root.destroy()


def p_key_pressed(event):
    global doReadFile, statusMsg
    statusMsg.set("Paused")
    doReadFile = False


def r_key_pressed(event):
    global doReadFile, statusMsg, doForward, doBack
    statusMsg.set("Running")
    doReadFile = True
    doForward = False
    doBack = False


def wait(dur):
    global root
    t0 = time.time()
    while((time.time()-t0)*1000 < dur):
        root.update_idletasks()
        root.update()


root = tk.Tk()
root.title("Textio Player")
root.geometry("1080x720")
root.update()
T = tk.Text(root, height=35, width=120)
T.pack()
infolabel = tk.Label(
    root, text="CONTROLS KEYS \n P - Pause \t R - Resume \t Q - Quit\n\nStatus:")
infolabel.pack()
statusMsg = tk.StringVar()
tk.Label(root, textvariable=statusMsg).pack()
statusMsg.set("Running")
root.bind("q", q_key_pressed)
root.bind("p", p_key_pressed)
root.bind("r", r_key_pressed)
root.update()

f = open(sys.argv[1], 'r')

render = ""
t0 = time.time()
pre_time = 0
doReadFile = True
doResume = False
waitTime = 0
lines = f.readlines()
line_number = 0
while(True):
    if doReadFile and line_number < len(lines):
        cur_time, diff, char = lines[line_number].split('|')
        cur_time = int(cur_time)
        wait(cur_time - pre_time)
        char = char[:-1]
        if diff == '+':
            char = literal_eval("b{}".format(char)).decode('unicode_escape')
            T.insert(tk.END, char)
        else:
            T.delete("end-2c")
        pre_time = cur_time
        line_number += 1
    if line_number >= len(lines):
        statusMsg.set("Finished")
    root.update_idletasks()
    root.update()
f.close()

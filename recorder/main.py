import diff_match_patch as dmp_module
import time
import tkinter as tk
from tkinter.filedialog import asksaveasfile


def save():
    global FileName, isFileCreated, varFileName, RecordBtn, FileBtn
    files = [('Textio Files', '*.tio*')]
    file = asksaveasfile(
        filetypes=files, defaultextension=files, initialfile="untitled.tio", mode="a+")
    FileName = file
    isFileCreated = True
    varFileName.set(FileName.name)
    RecordBtn["state"] = "normal"
    FileBtn["state"] = "disabled"


def startRecord():
    global startRecording, t0, RecordBtn, StopBtn
    startRecording = True
    t0 = time.time()
    T.configure(state="normal")
    RecordBtn["state"] = "disabled"
    StopBtn["state"] = "normal"


def stopAndQuit():
    root.destroy()
    if isFileCreated:
        FileName.close()


startRecording = False
isFileCreated = False
root = tk.Tk()
root.geometry("1080x720")

varFileName = tk.StringVar()
tk.Label(root, textvariable=varFileName).pack()

T = tk.Text(root, height=35, width=120)
T.configure(state="disabled")
T.pack()

FileBtn = tk.Button(root, text='Create New File', command=lambda: save())
FileBtn.pack()

RecordBtn = tk.Button(root, text='Start Recording',
                      command=lambda: startRecord())
RecordBtn.pack()

StopBtn = tk.Button(root, text='Stop and Quit', command=lambda: stopAndQuit())
StopBtn.pack()

RecordBtn["state"] = "disabled"
StopBtn["state"] = "disabled"

t0 = time.time()
res = "\n"
root.update()

while True:
    if startRecording and isFileCreated:
        new = T.get("1.0", "end")
        if res != new:
            t1 = int((time.time() - t0)*1000)
            diff = "-"
            if len(res) < len(new):
                diff = "+"
                char = new[-2]
                FileName.write("%s|%s|%s\n" % (t1, diff, repr(char)))
                FileName.seek(0)
            else:
                FileName.write("%s|%s|\n" % (t1, diff))
                FileName.seek(0)
            res = new
    root.update()
    root.update_idletasks()

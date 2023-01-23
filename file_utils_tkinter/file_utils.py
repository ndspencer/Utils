import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
from os.path import isfile, join
import re

root = tk.Tk()
root.title("File Utils")

directory = ""
label_dir_text = tk.StringVar(value="None")
regex_text = tk.StringVar()
replace_text = tk.StringVar()
def change_dir():
    global directory, file_list
    directory = filedialog.askdirectory()
    label_dir_text.set(directory)
    update_list()

regex_timer_id = ''
def regex_text_update(x):
    global regex_timer_id
    if regex_timer_id != '':
        root.after_cancel(regex_timer_id)
    regex_timer_id = root.after(1000, update_list)
    btn_rename['state'] = tk.DISABLED

def update_regex():
    global regex_timer_id
    regex_timer_id = ''
    label_dir_text.set(regex_text.get())

def update_list():
    file_list.delete(*file_list.get_children())
    files = [f for f in os.listdir(directory) if isfile(join(directory, f))]
    try:
        regex = re.compile(regex_text.get())
        valid = True
    except:
        valid = False
    for f in files:
        if valid:
            newf = regex.sub(replace_text.get(), f)
            if newf == f:
                newf = '<NO CHANGE>'
        else:
            newf = '<INVALID_REGEX>'
        file_list.insert('', 'end', values=(f, newf))
    btn_rename['state'] = tk.NORMAL

def do_rename():
    for child in file_list.get_children():
        os.chdir(directory)
        current, new = file_list.item(child)["values"]
        if new != '<INVALID_REGEX>' and new != '<NO CHANGE>':
            os.rename(current, new)
    update_list()

frm = ttk.Frame(root, padding=10)
frm.pack(fill='both', expand=1)
frm.columnconfigure(1, weight=99)

ttk.Button(frm, text="Directory", command=change_dir).grid(row=0, column=0, sticky='E')

ttk.Label(frm, textvariable=label_dir_text).grid(row=0, column=1, sticky='EW')

ttk.Label(frm, text='Regex Capture').grid(row=1, column=0, sticky='E')
entry_regex = ttk.Entry(frm, textvariable=regex_text)
entry_regex.bind('<KeyRelease>', regex_text_update)
entry_regex.grid(row=1, column=1, sticky='EW')

ttk.Label(frm, text='Regex Subsitution').grid(row=2, column=0, sticky='E')
entry_replace = ttk.Entry(frm, textvariable=replace_text)
entry_replace.bind('<KeyRelease>', regex_text_update)
entry_replace.grid(row=2, column=1, sticky='EW')

file_list = ttk.Treeview(frm, columns=('before', 'after'), show='headings')
file_list.heading("before", text="before")
file_list.heading('after', text='after')
file_list.grid(row=3, column=0, columnspan=2, sticky='NSEW')
frm.rowconfigure(3, weight=99)
file_list.insert('', 'end', values=('one', 'two'))

btn_rename = ttk.Button(frm, text="Rename Files", command=do_rename)
btn_rename.grid(row=4, column=0, columnspan=2)
btn_rename['state'] = tk.DISABLED

root.mainloop()
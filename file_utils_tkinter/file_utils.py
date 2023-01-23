import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from os import listdir
from os.path import isfile, join
import re

root = tk.Tk()
root.title("File Utils")

directory = ""
label_dir_text = tk.StringVar(value="Directory: None")
regex_text = tk.StringVar()
replace_text = tk.StringVar()
def change_dir():
    global directory, file_list
    directory = filedialog.askdirectory()
    label_dir_text.set("Directory: {}".format(directory))
    update_list()

regex_timer_id = ''
def regex_text_update(x):
    global regex_timer_id
    if regex_timer_id != '':
        root.after_cancel(regex_timer_id)
    regex_timer_id = root.after(1000, update_list)

def update_regex():
    global regex_timer_id
    regex_timer_id = ''
    label_dir_text.set(regex_text.get())

def update_list():
    file_list.delete(*file_list.get_children())
    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    for f in files:
        newf = re.sub(regex_text.get(), replace_text.get(), f)
        file_list.insert('', 'end', values=(f, newf))


frm = ttk.Frame(root, padding=10)
frm.pack()

ttk.Button(frm, text="Change Directory", command=change_dir).pack()

ttk.Label(frm, textvariable=label_dir_text).pack()

entry_regex = ttk.Entry(frm, textvariable=regex_text)
entry_regex.bind('<KeyRelease>', regex_text_update)
entry_regex.pack()

entry_replace = ttk.Entry(frm, textvariable=replace_text)
entry_replace.bind('<KeyRelease>', regex_text_update)
entry_replace.pack()

ttk.Button(frm, text="Rename Files", command=update_regex).pack()

file_list = ttk.Treeview(frm, columns=('before', 'after'), show='headings')
file_list.heading("before", text="before")
file_list.heading('after', text='after')
file_list.pack()

file_list.insert('', 'end', values=('one', 'two'))

root.mainloop()
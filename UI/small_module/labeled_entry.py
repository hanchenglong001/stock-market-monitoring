from tkinter import  Label, Frame,Entry


def add_labeled_entry(parent_window,label_text):
    frame = Frame(parent_window)
    frame.pack(padx=10, pady=5, fill='x')
    Label(frame, text=label_text).pack(side='left')
    entry = Entry(frame)
    entry.pack(side='left', expand=True, fill='x')
    return entry

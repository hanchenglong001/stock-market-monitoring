import tkinter as tk
import webbrowser

def open_webpage():
    webbrowser.open("https://52etf.site/")

root = tk.Tk()
button = tk.Button(root, text="Open Web Page", command=open_webpage)
button.pack(padx=20, pady=20)

root.mainloop()

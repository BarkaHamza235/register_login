from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import time
import os


class Employe:
    def __init__(self, root):
        self.root = root
        self.root.title("Employe")
        self.root.geometry("1920x1040+0+0")
        self.root.config(bg="white")
        self.root.focus_force()
        
        


if __name__=="__main__":
    root = Tk()
    obj = Employe(root)
    root.mainloop()
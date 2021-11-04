from tkinter import *
from PIL import ImageTk, Image
import glob


class ImageListBox:
    def __init__(self, root, folder):
        self.files = glob.glob(folder + "/*.png")

        self.l = Listbox(root, width=30, height=5)
        self.l.pack()
        self.l.bind("<<ListboxSelect>>", self.imageShow)

        self.c = Label(root)
        self.c.pack()

        for f in self.files:
            self.l.insert(END, f)

    def imageShow(self, event):
        path = self.files[self.l.curselection()[0]]
        img = ImageTk.PhotoImage(Image.open(path).resize((80, 80)))
        self.c.image = img
        self.c.configure(image=img)
        self.c.pack()

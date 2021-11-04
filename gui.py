from tkinter import *
import tkinter.ttk
from PIL import ImageTk, Image

from imageListBox import ImageListBox

# Window config
root = Tk()
root.title("Synthetic fingerprint to photo")

icon = PhotoImage(file="./fingerprint-icon.png")
root.iconphoto(False, icon)

# Methods
def importImage():
    print("Import clicked.")  # TODO: remake


def saveImage():
    print("Save clicked.")  # TODO: remake


### Fingerprint section ###


fingerprint = Image.open("./SG_1_1_sq.png")
fingerprint.thumbnail((700, 700))
fingerprint = ImageTk.PhotoImage(fingerprint)
fingerprintLabel = Label(root, text="Fingerprint", font=("Helvetica", 16, "bold"))
fingerprintImage = Label(root, image=fingerprint)

fingerprintLabel.grid(row=0, column=0, pady=(10, 15))
fingerprintImage.grid(row=1, column=0, padx=(15, 15), rowspan=20)

importButton = Button(
    root,
    text="Import",
    font=("Helvetica", 11, "bold"),
    padx=40,
    border=0,
    bg="#03a9f4",
    fg="white",
    command=importImage,
)
importButton.grid(row=21, column=0, pady=(15, 15))


### Photo section ###


photo = Image.open("./skin_texture_1.png")
photo.thumbnail((500, 500))
photo = ImageTk.PhotoImage(photo)
photoLabel = Label(root, text="Photo", font=("Helvetica", 16, "bold"))
photoImage = Label(root, image=photo)

photoLabel.grid(row=0, column=1, pady=(10, 15))
photoImage.grid(row=1, column=1, padx=(15, 15), rowspan=20)

saveButton = Button(
    root,
    text="Save",
    font=("Helvetica", 11, "bold"),
    padx=40,
    border=0,
    bg="#43a047",
    fg="white",
    command=saveImage,
)
saveButton.grid(row=21, column=1, pady=(15, 15))


### Panel section ###


tkinter.ttk.Separator(root, orient=VERTICAL).grid(
    column=3, row=0, rowspan=25, sticky="ns"
)
panelLabel = Label(root, text="Preferences", font=("Helvetica", 16, "bold"))
panelLabel.grid(row=0, column=4, pady=(10, 15))

# Fingerprint frame
fingerprintFrame = LabelFrame(
    root, text="Fingerprint", font=("Helvetica", 11), padx=5, pady=5
)
fingerprintFrame.grid(row=1, column=4, rowspan=5, padx=10, pady=10)

fingerprintListBox = ImageListBox(fingerprintFrame, "./assets/fingerprints")

# Skin frame
skinFrame = LabelFrame(root, text="Skin", font=("Helvetica", 11), padx=5, pady=5)
skinFrame.grid(row=6, column=4, rowspan=5, padx=10, pady=10)

skinListBox = ImageListBox(skinFrame, "./assets/skins")

# Background frame
backgroundFrame = LabelFrame(
    root, text="Background", font=("Helvetica", 11), padx=5, pady=5
)
backgroundFrame.grid(row=11, column=4, rowspan=5, padx=10, pady=10)

backgroundListBox = ImageListBox(backgroundFrame, "./assets/backgrounds")

### Main loop ###
root.mainloop()

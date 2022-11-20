import tkinter as tk
# import the necessary packages
from tkinter import *
from tkinter import filedialog as tkFileDialog
from multiple_roi import select_rois

# https://www.pythontutorial.net/tkinter/tkinter-validation/

class ImgInfo:
    def __init__(self, w, h):
        self.width = w
        self.height = h


def select_path():
    # choose file path
    path = tkFileDialog.askopenfilename()

    if inputtxt_height.get(1.0, "end-1c") != "" and inputtxt_height.get(1.0, "end-1c") != "":
        img_info = ImgInfo(inputtxt_width.get(1.0, "end-1c"), inputtxt_height.get(1.0, "end-1c"))

    if len(path) > 0:
        print(path)
        select_rois(path)


window = tk.Tk()
window.title('Main window')
window.geometry('500x300')

# Create label
width_label = Label(window, text="Enter width")
width_label.config(font=("Courier", 14))
# TextBox Creation
inputtxt_width = tk.Text(window, height=1, width=20)
# Create label
height_label = Label(window, text="Enter height")
height_label.config(font=("Courier", 14))
inputtxt_height = tk.Text(window, height=1, width=20)

width_label.pack()
inputtxt_width.pack()
height_label.pack()
inputtxt_height.pack()

tk.Button(window, text="select path to video", command=select_path).pack()

window.mainloop()
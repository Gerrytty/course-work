import tkinter as tk
# import the necessary packages
# from tkinter import *
from tkinter import filedialog as tkFileDialog

from tkinter.ttk import *

import numpy as np

from multiple_roi import select_points, read_img
from read_video import read_video

import matplotlib.pyplot as plt

import pandas as pd

# https://www.pythontutorial.net/tkinter/tkinter-validation/


class ImgInfo:
    def __init__(self, w, h):
        self.width = w
        self.height = h


def select_path():
    # choose file path
    path = tkFileDialog.askopenfilename()

    img_info = None

    if inputtxt_width.get(1.0, "end-1c") != "":
        img_info = ImgInfo(inputtxt_width.get(1.0, "end-1c"), inputtxt_height.get(1.0, "end-1c"))
        try:
            w = int(img_info.width)
            img_info.width = w
            print(w)
        except Exception:
            img_info = None
            print("Can't cast to int")

    if len(path) > 0:
        print(path)
        # path = "/home/julia/occlusion-tracker/simple_test/out.png"
        areas, img_raw = read_img(path)

        areas_dict = {}

        for i, area in enumerate(areas):
            area_title = f"сегмент {i} ({area.choosen_point[0]}, {area.choosen_point[1]})"

            distances = np.array(area.distances)

            if img_info is not None:
                one_pixel_size = img_info.width / img_raw.shape[0]

                print(f"One pixel size {one_pixel_size}")

                distances *= one_pixel_size
                area.distances = list(distances)

            areas_dict[area_title] = area.distances

            y_label = "см"

            if img_info is None:
                y_label = "пиксель"

            plt.title(f"Roi {i}")
            plt.xlabel("Кадр")
            plt.ylabel(y_label)
            plt.plot(area.distances, label=f"Roi {i}")

        plt.legend()
        plt.show()

        csv_name = path.split("/")[-1].split(".")[0]

        df = pd.DataFrame(areas_dict)
        df.index.name = "Frame"
        df.to_csv(f"{csv_name}.csv")


window = tk.Tk()

style = Style(window)
print(style.theme_names())
print(style.theme_use())
style.theme_use(style.theme_names()[0])

window.title('Main window')
window.geometry('700x200')

# Create label
width_label = Label(window, text="Введите ширину видео (см)")
width_label.config(font=("Courier", 14))
# TextBox Creation
inputtxt_width = tk.Text(window, height=1, width=20)
# Create label
height_label = Label(window, text="Enter height")
height_label.config(font=("Courier", 14))
inputtxt_height = tk.Text(window, height=1, width=20)

spacer1 = tk.Label(window, text="")
# spacer1.grid(row=4, column=0)

# width_label.pack()
# inputtxt_width.pack()
# height_label.pack()
# inputtxt_height.pack()

button = tk.Button(window, text="Выбрать путь", command=select_path)
# button.grid(row=0, column=1, padx=10, pady=10)

width_label.pack()
inputtxt_width.pack()
spacer1.pack()
button.pack()

window.mainloop()
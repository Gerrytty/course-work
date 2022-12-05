import cv2
from plantcv import plantcv as pcv
import numpy as np
from clusters import get_distance
import matplotlib.pyplot as plt
import json
import pandas as pd
import datetime as dt
from screeninfo import get_monitors
import matplotlib.animation as animation


# todo filter outliers
# todo multiple points in one roi
# todo multiple graphics in one canvas
# todo real time (optimal) (choose camera)
# todo x axis as seconds
# todo add choice for map pixels to mm/cm (variable choice)
# todo exec file


def get_first_frame(path):
    cap = cv2.VideoCapture(path)

    if not cap.isOpened():
        raise ValueError("Video is not found")

    fps = cap.get(cv2.CAP_PROP_FPS)

    if cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # todo fix this
        # frame = cv2.resize(frame, (get_monitors()[0].width // 2, get_monitors()[0].height // 2))

        if ret:
            return frame, cap, fps


current_frame = 0

def read_video(cap, areas, fps):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    xs = []
    ys = []

    yss = [[] for i in range(len(areas))]

    def get_dist(k, xs, yss, cap, areas):
        ret, img_raw = cap.read()
        if ret:
            img_raw = cv2.cvtColor(img_raw, cv2.COLOR_RGB2GRAY)

            global current_frame
            current_frame += 1
            xs.append(current_frame / fps)

            print(f"Len of areas = {len(areas)}")

            ax.clear()

            for i, area in enumerate(areas):
                img_crop = np.array(img_raw[int(area.r2):int(area.r2 + area.r4), int(area.r1):int(area.r1 + area.r3)])
                canny = pcv.canny_edge_detect(img=img_crop, sigma=area.sigma, low_thresh=area.lower_trash,
                                              high_thresh=area.upper_trash)
                nearest_point_in_first_cluster, nearest_point_in_second_cluster, distance = get_distance(
                    area.choosen_point,
                    canny)
                area.distances.append(distance)
                yss[i].append(area.distances[-1])

                # Draw x and y lists
                ax.plot(xs[-100:], yss[i][-100:])

                # todo
                plt.xlabel('Пиксель')
                plt.ylabel('Секунды')


    # Set up plot to call animate() function periodically
    ani = animation.FuncAnimation(fig, get_dist, fargs=(xs, yss, cap, areas), interval=0)
    plt.show()

    return areas
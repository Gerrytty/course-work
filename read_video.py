import cv2
from plantcv import plantcv as pcv
import numpy as np
from clusters import get_distance
import matplotlib.pyplot as plt


def get_first_frame(path):
    cap = cv2.VideoCapture(path)

    if not cap.isOpened():
        raise ValueError("Video is not found")

    if cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        if ret != -1:
            return frame, cap


def read_video(cap, areas):

    i = 1
    while cap.isOpened():

        print(f"current frame = {i}")

        i += 1

        ret, img_raw = cap.read()

        if ret:
            img_raw = cv2.cvtColor(img_raw, cv2.COLOR_RGB2GRAY)
            for area in areas:
                img_crop = np.array(img_raw[int(area.r2):int(area.r2 + area.r4), int(area.r1):int(area.r1 + area.r3)])
                canny = pcv.canny_edge_detect(img=img_crop, sigma=area.sigma, low_thresh=area.lower_trash, high_thresh=area.upper_trash)
                nearest_point_in_first_cluster, nearest_point_in_second_cluster, distance = get_distance(area.choosen_point,
                                                                                                         canny)

                area.distances.append(distance)

        else:
            break

    for area in areas:
        plt.plot(area.distances)
        plt.show()

    print(areas)

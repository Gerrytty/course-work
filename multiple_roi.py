import cv2
import numpy as np
from area import Area
from plantcv import plantcv as pcv
from clusters import *


def callback(x):
    pass


def select_rois(img_path):
    points = []

    def select_point(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            points.append((x, y))

    # read image
    img_raw = cv2.imread(img_path)
    img_raw = cv2.resize(img_raw, (1440, 900))
    cv2.namedWindow("roi")

    count_of_roi = 0

    while True:

        rois_array = []

        ROIs = cv2.selectROI("roi", img_raw, showCrosshair=True)
        key = cv2.waitKey(10)

        if sum(ROIs) == 0:
            cv2.destroyAllWindows()
            break

        img_crop = np.array(img_raw[int(ROIs[1]):int(ROIs[1] + ROIs[3]), int(ROIs[0]):int(ROIs[0] + ROIs[2])])
        cv2.namedWindow(f"roi_{count_of_roi}")

        cv2.createTrackbar('Lower trash', f'roi_{count_of_roi}', 0, 255, callback)
        cv2.createTrackbar('Upper trash', f"roi_{count_of_roi}", 0, 255, callback)
        cv2.createTrackbar('Sigma', f"roi_{count_of_roi}", 1, 20, callback)
        cv2.setMouseCallback(f"roi_{count_of_roi}", select_point)

        area = Area(*ROIs, img_crop)

        canny = pcv.canny_edge_detect(img=img_crop, sigma=0.1, low_thresh=0, high_thresh=0)

        cv2.imshow(f"roi_{count_of_roi}", canny)

        wait_time = 10
        while cv2.getWindowProperty(f"roi_{count_of_roi}", cv2.WND_PROP_VISIBLE) >= 1:

            if len(points) > count_of_roi:
                cv2.circle(canny, (points[-1][0], points[-1][1]), 1, (255, 0, 0), -1)

                if area.nearest_point_in_first_cluster is not None and area.nearest_point_in_second_cluster is not None:
                    cv2.circle(canny, (
                    int(area.nearest_point_in_first_cluster[0]), int(area.nearest_point_in_first_cluster[1])), 2,
                               (255, 0, 0), -1)
                    cv2.circle(canny, (
                    int(area.nearest_point_in_second_cluster[0]), int(area.nearest_point_in_second_cluster[1])), 2,
                               (255, 0, 0), -1)

                if area.choosen_point is None:
                    area.choosen_point = (points[-1][0], points[-1][1])

                    nearest_point_in_first_cluster, nearest_point_in_second_cluster, distance = get_distance(points[-1],
                                                                                                             canny)
                    area.nearest_point_in_first_cluster = nearest_point_in_first_cluster
                    area.nearest_point_in_second_cluster = nearest_point_in_second_cluster

                    print(distance)

            cv2.imshow(f"roi_{count_of_roi}", canny)
            keyCode = cv2.waitKey(wait_time)
            if (keyCode & 0xFF) == ord("q"):
                cv2.destroyAllWindows()
                break

            lower = cv2.getTrackbarPos('Lower trash', f"roi_{count_of_roi}")
            upper = cv2.getTrackbarPos('Upper trash', f"roi_{count_of_roi}")
            sigma = cv2.getTrackbarPos("Sigma", f"roi_{count_of_roi}")

            area.lower_trash = lower
            area.upper_trash = upper
            area.sigma = sigma

            canny = pcv.canny_edge_detect(img=img_crop, sigma=sigma, low_thresh=lower, high_thresh=upper)

        rois_array.append(area)

        count_of_roi += 1

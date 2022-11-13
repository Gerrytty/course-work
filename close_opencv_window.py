import cv2

img = cv2.imread("/home/julia/Pictures/Wallpapers/2022-09-30-buck-1-54010.jpg")
cv2.namedWindow("just_a_window")
cv2.imshow("just_a_window", img)

wait_time = 10
while cv2.getWindowProperty('just_a_window', cv2.WND_PROP_VISIBLE) >= 1:
    keyCode = cv2.waitKey(wait_time)
    if (keyCode & 0xFF) == ord("q"):
        cv2.destroyAllWindows()
        break

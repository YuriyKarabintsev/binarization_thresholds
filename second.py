import cv2
import numpy as np


def nothing():
    pass


cv2.namedWindow("Trackbar")

cv2.createTrackbar("minb", "Trackbar", 0, 255, nothing)
cv2.createTrackbar("ming", "Trackbar", 0, 255, nothing)
cv2.createTrackbar("minr", "Trackbar", 0, 255, nothing)
cv2.createTrackbar("maxb", "Trackbar", 0, 255, nothing)
cv2.createTrackbar("maxg", "Trackbar", 0, 255, nothing)
cv2.createTrackbar("maxr", "Trackbar", 0, 255, nothing)

Background_img = cv2.imread("try.png")
cv2.imshow("Trackbar", Background_img)

cap = cv2.VideoCapture(0)
ESCAPE = 27
key = 1

noDrive = cv2.imread("parking.jpg")
noDrive_bin = cv2.inRange(noDrive, (0, 0, 0), (231, 255, 255))
noDrive_bin = cv2.resize(noDrive_bin, (64, 64))

ped = cv2.imread("pedestrian.jpg")
ped_bin = cv2.inRange(noDrive, (0, 0, 0), (240, 240, 240))
ped_bin = cv2.resize(noDrive_bin, (64, 64))

while (key != ESCAPE):
    ret, frame = cap.read()
    #cv2.imshow("frame", frame)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.blur(hsv, (5, 5)) # (5, 5) - размер ядра свёртки
    mask = cv2.inRange(hsv, (0, 0, 0), (255, 255, 255))
    cv2.imshow("Mask", mask)

    #mask = cv2.erode(mask, None, iterations=5) # iterations - кол-во повторений функции. Эта функция убирает единичные белые пиксели

    #mask = cv2.dilate(mask, None, iterations=4)
    # dilate аналогична erode, но она

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        frame_viz = frame.copy()
        cv2.drawContours(frame_viz, contours, 0, (255, 0, 255), 3)
        cv2.imshow("Contour", frame_viz)
        (x, y, w, h) = cv2.boundingRect(contours[0])
        cv2.rectangle(frame_viz, (x, y, x + w, y + h), (255, 255, 0), thickness=2)
        detected_sign = frame[y: y + h, x: x + w]

        detected_sign_bin = mask[y: y + h, x: x + w]
        detected_sign_bin = cv2.resize(detected_sign_bin, (64, 64))

        noDrive_val = 0
        arr1 = [23, 45, 56]
        arr2 = [23, 41, 56]
        #arr1[True, False, True] = 1

        zeros_arr = np.zeros((64, 64))
        zeros_arr[detected_sign_bin == noDrive_bin] = 1
        noDrive_val = np.sum(zeros_arr)

        zeros_arr = np.zeros((64, 64))
        zeros_arr[detected_sign_bin == ped_bin] = 1
        ped_val = np.sum(zeros_arr)
        arr1 < arr2
        #for i in range(64):
        #    for j in range(64):
        #        if detected_sign_bin[i, j] == noDrive_bin[i, j]:
        #            noDrive_val += 1


        print(noDrive_val, ped_val)
        if noDrive_val >= 3500:
            print("NoDrive")
        else:
            print("No object")


    key = cv2.waitKey(10)

cap.release()
cv2.destroyAllWindows()
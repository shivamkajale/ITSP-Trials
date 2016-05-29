import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(0)
cv2.namedWindow('Parameters')

cv2.createTrackbar('Hue','Parameters',0,255,nothing)
cv2.createTrackbar('Sat','Parameters',0,255,nothing)
cv2.createTrackbar('Val','Parameters',0,255,nothing)

while(1):

    # Take each frame
    ret , frameinv = cap.read()
    frame=cv2.flip(frameinv ,1)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    hue = cv2.getTrackbarPos('Hue','Parameters')
    sat = cv2.getTrackbarPos('Sat','Parameters')
    val = cv2.getTrackbarPos('Val','Parameters')
    # define range of blue color in HSV
    lower = np.array([hue-20,sat,val])
    upper = np.array([hue+20,255,255])


    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower, upper)

    # Bitwise-AND mask and original imaget
    res = cv2.bitwise_and(frame ,frame, mask= mask)


#    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

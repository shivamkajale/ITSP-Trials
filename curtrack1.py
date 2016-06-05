import cv2
import numpy as np
import pyautogui

def nothing(x):
    pass

def swap( array, i, j):
    temp = array[i]
    array[i] = array[j]
    array[j] = temp

cap = cv2.VideoCapture(0)
cv2.namedWindow('Parameters')
'''
cv2.createTrackbar('Hue','Parameters',0,255,nothing)
cv2.createTrackbar('Sat','Parameters',0,255,nothing)
cv2.createTrackbar('Val','Parameters',0,255,nothing)
'''
center=(0,0)

while(1):

    # Take each frame
    ret , frameinv = cap.read()
    frame=cv2.flip( frameinv, 1)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

#    hue = cv2.getTrackbarPos('Hue','Parameters')
 #   sat = cv2.getTrackbarPos('Sat','Parameters')
  #  val = cv2.getTrackbarPos('Val','Parameters')
    # define range of blue color in HSV
    lower = np.array([100,70,10])
    upper = np.array([140,255,255])


    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower, upper)
    _, contour, _ = cv2.findContours( mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#   blurmask = cv2.GaussianBlur( mask, (5,5), 0)
#  _, contourb, _ = cv2.findContours( blurmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    area = np.zeros([len(contour)])

    for i in range(len(contour)):
        area[i] = cv2.contourArea(contour[i])

    a = sorted(area,reverse=True)
    
    for i in range(len(contour)):
        for j in range(1):
            if area[i] == a[j]:
                swap(contour, i, j)
    '''   
    area = np.zeros([len(contourb)])

    for i in range(len(contourb)):
        area[i] = cv2.contourArea(contourb[i])

    a = sorted(area,reverse=True)
    
    for i in range(len(contourb)):
        for j in range(1):
            if area[i] == a[j]:
                swap(contourb, i, j)
    '''
    if len(contour)>0:
        rect = cv2.minAreaRect(contour[0])
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        c = rect[0]
        pre_center = center
        center = np.array([int(c[0]),int(c[1])])
#        print center
        cv2.circle(frame, (int(c[0]),int(c[1])), 3, (0,255,255), -1)
        ellipse = cv2.fitEllipse(contour[0])
        cv2.ellipse(frame,ellipse,(0,0,255),2)
        if(abs(pre_center[0]-center[0])>3 and abs(pre_center[1]-center[1])>3):
            pyautogui.moveTo(3*center[0],3*center[1],)


#    vidContb = cv2.drawContours( frame, contourb[0:2], -1, (0,255,0), 2)
    vidCont = cv2.drawContours( frame, [box], 0, (0,255,0), 2)
    # Bitwise-AND mask and original imaget
    res = cv2.bitwise_and(frame ,frame, mask= mask)


#    cv2.imshow('contb', vidContb)
    cv2.imshow('cont', vidCont)
#    cv2.imshow('res',res)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
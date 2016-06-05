import cv2
import numpy as np
import pyautogui
import time

blue_range = np.array([[100,75,18],[140,255,255]])
yellow_range = np.array([[7,90,135],[47,255,255]])
green_range = np.array([[65,75,65],[105 ,255,255]])
b_cen, y_cen, g_cen = [240,320],[240,320],[240,320]

def nothing():
	pass

def swap( array, i, j):
    temp = array[i]
    array[i] = array[j]
    array[j] = temp

def makeMask(hsv_frame, color_Range):
	return cv2.inRange( hsv_frame, color_Range[0], color_Range[1])

def drawCentroid(vid, mask):
	_, contour, _ = cv2.findContours( mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	area = np.zeros([len(contour)])
	l=len(contour)
	for i in range(l):
		area[i] = cv2.contourArea(contour[i])

	a = sorted( area, reverse=True)	

	for i in range(l):
		for j in range(1):
			if area[i] == a[j]:
				swap( contour, i, j)

	if l > 0 :

		M = cv2.moments(contour[0])
		if M['m00'] != 0:
			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])
			center = (cx,cy)

			cv2.circle( vid, center, 5, (0,0,255), -1)
					
			return center
	else:
		return -1
#        if(abs(pre_center[0]-center[0])>3 and abs(pre_center[1]-center[1])>3):
 #           pyautogui.moveTo(3*center[0],3*center[1],)


cap = cv2.VideoCapture(0)

while(1):

	_, frameinv = cap.read()
	frame = cv2.flip( frameinv, 1)

	hsv = cv2.cvtColor( frame, cv2.COLOR_BGR2HSV)

	b_mask = makeMask( hsv, blue_range)
	g_mask = makeMask( hsv, green_range)
	y_mask = makeMask( hsv, yellow_range)

	pre_g_cen = g_cen

	b_cen = drawCentroid( frame, b_mask)
	g_cen = drawCentroid( frame, g_mask)
	y_cen = drawCentroid( frame, y_mask)

	if b_cen != -1 and g_cen != -1 and y_cen != -1:
		if abs(pre_g_cen[0]-g_cen[0])>1 and abs(pre_g_cen[1]-g_cen[1])>1:
			if g_cen[0]>120 and g_cen[0]<600 and g_cen[1]>80 and g_cen[1]<350:
				pyautogui.moveTo( 4*(g_cen[0]-120), 4*(g_cen[1]-80),duration=.05)
#				pyautogui.moveTo( 4*(g_cen[0]-120), 4*(g_cen[1]-80))				
		
		elif g_cen[0]<120 and g_cen[1]>80 and g_cen[1]<350:
			pyautogui.moveTo( 5, 4*(g_cen[1]-80))
		elif g_cen[0]>600 and g_cen[1]>80 and g_cen[1]<350:
			pyautogui.moveTo( 1915, 4*(g_cen[1]-80))
		elif g_cen[0]>80 and g_cen[0]<600 and g_cen[1]<80:
			pyautogui.moveTo( 4*(g_cen[0]-120), 5) 
		elif g_cen[0]>120 and g_cen[0]<600 and g_cen[1]>350:
			pyautogui.moveTo( 4*(g_cen[0]-120), 1075)
		
		if y_cen[0]>(b_cen[0]+10):
			pyautogui.click(button='right')
			time.sleep(.5)
		elif abs(y_cen[0]-b_cen[0])<20 and abs(y_cen[1]-b_cen[1])<50:
			pyautogui.click()
			time.sleep(.5) 
		
	cv2.imshow('Frame', frame)

	k = cv2.waitKey(1) & 0xFF
	if k == 27:
		break

cv2.destroyAllWindows()
    
        






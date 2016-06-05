import cv2
import numpy as np
import pyautogui

blue_range = np.array([[100,97,18],[140,255,255]])
yellow_range = np.array([[7,90,135],[47,255,255]])
green_range = np.array([[45,66,30],[85 ,255,255]])
b_cen, y_cen, g_cen = [240,320],[240,320],[240,320]

def nothing():
	pass

def swap( array, i, j):
    temp = array[i]
    array[i] = array[j]
    array[j] = temp

def makeMask(hsv_frame, color_Range):
	return cv2.inRange( hsv_frame, color_Range[0], color_Range[1])

def drawEllipse(vid, mask):
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

	if l > 0 and cv2.fitEllipse(contour[0]):
		ellipse = cv2.fitEllipse(contour[0])
		c = ellipse[0]
#		pre_center = center
		center = np.array([int(c[0]),int(c[1])])

		cv2.circle( vid, (int(c[0]),int(c[1])), 3, (0,255,255), -1)
		ellipse = cv2.fitEllipse(contour[0])
		cv2.ellipse( vid, ellipse, (0,0,255), 2)			
		return ellipse[0]

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
	b_cen = drawEllipse( frame, b_mask)
	g_cen = drawEllipse( frame, g_mask)
	y_cen = drawEllipse( frame, y_mask)

	pyautogui.moveTo( 3*b_cen[0], 3*b_cen[1])
	if abs(y_cen[0]-g_cen[0])<50 and abs(y_cen[1]-g_cen[1])<50:
		pyautogui.click() 

	cv2.imshow('Frame', frame)

	k = cv2.waitKey(1) & 0xFF
	if k == 27:
		break

cv2.destroyAllWindows()
    
        






# All packages needed for the program are imported ahead
import cv2
import numpy as np
import pyautogui
import time
from win32api import GetSystemMetrics

# Some global variables or others that need prior intialization are initalized here

# colour ranges for feeding to the inRange funtions 
blue_range = np.array([[88,78,20],[128,255,255]])
yellow_range = np.array([[21,125,94],[61,255,255]])
red_range = np.array([[158,85,72],[180 ,255,255]])

# Prior initialization of all centers for safety
b_cen, y_pos, r_cen = [240,320],[240,320],[240,320]
cursor = [960,540]

# Area ranges for contours of different colours to be detected
r_area = [00,1700]
b_area = [00,1700]
y_area = [00,17000]

# Rectangular kernal for eroding and dilating the mask for primary noise removal 
kernel = np.ones((7,7),np.uint8)

# Status variables defined globally
perform = False
showCentroid = False

# 'nothing' function is useful when creating trackbars
# It is passed as last arguement in the cv2.createTrackbar() function
def nothing(x):
	pass

# To bring to the top the contours with largest area in the specified range
# Used in drawContour()
def swap( array, i, j):
	temp = array[i]
	array[i] = array[j]
	array[j] = temp

# To toggle status of control variables
def changeStatus(key):
	global perform
	global showCentroid
	global yellow_range,red_range,blue_range
	# toggle mouse simulation
	if key == ord('p'):
		perform = not perform
		if perform:
			print 'Mouse simulation ON...'
		else:
			print 'Mouse simulation OFF...'
	
	# toggle display of centroids
	elif key == ord('c'):
		showCentroid = not showCentroid
		if showCentroid:
			print 'Showing Centroids...'
		else:
			print 'Not Showing Centroids...'

	elif key == ord('r'):
		print '**********************************************************************'
		print '	You have entered recalibration mode.'
		print '	Present settings are visible on the trackbars.'
		print ' Use the trackbars to calibrate and press SPACE when done.'
		print '**********************************************************************'

		yellow_range = calibrateColor('Yellow', yellow_range)
		red_range = calibrateColor('Red', red_range)
		blue_range = calibrateColor('Blue', blue_range)			
	
	else:
		pass

# cv2.inRange function is used to filter out a particular color from the frame
# The result then undergoes morphosis i.e. erosion and dilation
# Resultant frame is returned as mask 
def makeMask(hsv_frame, color_Range):
	
	mask = cv2.inRange( hsv_frame, color_Range[0], color_Range[1])
	# Morphosis next ...
	eroded = cv2.erode( mask, kernel, iterations=1)
	dilated = cv2.dilate( eroded, kernel, iterations=1)
	
	return dilated

# Contours on the mask are detected.. Only those lying in the previously set area 
# range are filtered out and the centroid of the largest of these is drawn and returned 
def drawCentroid(vid, color_area, mask, showCentroid):
	
	_, contour, _ = cv2.findContours( mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	l=len(contour)
	area = np.zeros(l)

	# filtering contours on the basis of area rane specified globally 
	for i in range(l):
		if cv2.contourArea(contour[i])>color_area[0] and cv2.contourArea(contour[i])<color_area[1]:
			area[i] = cv2.contourArea(contour[i])
		else:
			area[i] = 0
	
	a = sorted( area, reverse=True)	

	# bringing contours with largest valid area to the top
	for i in range(l):
		for j in range(1):
			if area[i] == a[j]:
				swap( contour, i, j)

	if l > 0 :		
		# finding centroid using method of 'moments'
		M = cv2.moments(contour[0])
		if M['m00'] != 0:
			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])
			center = (cx,cy)
			if showCentroid:
				cv2.circle( vid, center, 5, (0,0,255), -1)
					
			return center
	else:
		# return error handling values
		return (-1,-1)

# This function helps in filtering the required colored objects from the background
def calibrateColor(color, def_range):
	
	global kernel
	name = 'Calibrate '+ color
	cv2.namedWindow(name)
	cv2.createTrackbar('Hue', name, def_range[0][0]+20, 180, nothing)
	cv2.createTrackbar('Sat', name, def_range[0][1], 255, nothing)
	cv2.createTrackbar('Val', name, def_range[0][2], 255, nothing)
	while(1):
		ret , frameinv = cap.read()
		frame=cv2.flip(frameinv ,1)

		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		hue = cv2.getTrackbarPos('Hue', name)
		sat = cv2.getTrackbarPos('Sat', name)
		val = cv2.getTrackbarPos('Val', name)

		lower = np.array([hue-20,sat,val])
		upper = np.array([hue+20,255,255])

		mask = makeMask(frame, np.array([lower,upper]))

		cv2.imshow(name, mask)

		k = cv2.waitKey(5) & 0xFF
		if k == ord(' '):
			cv2.destroyWindow(name)
			return np.array([[hue-20,sat,val],[hue+20,255,255]])


'''
This function takes as input the center of yellow region (yc) and 
the previous cursor position (pyp). The new cursor position is calculated 
in such a way that the mean deviation for desired steady state is reduced.
'''
def setCursorPos( yc, pyp):
	
	yp = np.zeros(2)
	
	if abs(yc[0]-pyp[0])<5 and abs(yc[1]-pyp[1])<5:
		yp[0] = yc[0] + .7*(pyp[0]-yc[0]) 
		yp[1] = yc[1] + .7*(pyp[1]-yc[1])
	else:
		yp[0] = yc[0] + .1*(pyp[0]-yc[0])
		yp[1] = yc[1] + .1*(pyp[1]-yc[1])
	
	return yp

# Movement of cursor on screen and clicking are controlled here  
def performAction( yp, rc, bc, perform):
	
	if perform :
		
		cursor[0] = 4*(yp[0]-110)
		cursor[1] = 4*(yp[1]-120)

		if yp[0]>110 and yp[0]<590 and yp[1]>120 and yp[1]<390:
			pyautogui.moveTo(cursor[0],cursor[1])
		elif yp[0]<110 and yp[1]>120 and yp[1]<390:
			pyautogui.moveTo( 8 , cursor[1])
		elif yp[0]>590 and yp[1]>120 and yp[1]<390:
			pyautogui.moveTo(1912, cursor[1])
		elif yp[0]>110 and yp[0]<590 and yp[1]<120:
			pyautogui.moveTo(cursor[0] , 8)
		elif yp[0]>110 and yp[0]<590 and yp[1]>390:
			pyautogui.moveTo(cursor[0] , 1072)
		elif yp[0]<110 and yp[1]<120:
			pyautogui.moveTo(8, 8)
		elif yp[0]<110 and yp[1]>390:
			pyautogui.moveTo(8, 1072)
		elif yp[0]>590 and yp[1]>390:
			pyautogui.moveTo(1912, 1072)
		else:
			pyautogui.moveTo(1912, 8)

		if rc[0]!=-1 and bc[0]!=-1:
			if abs(rc[0]-bc[0])<35 and abs(rc[1]-bc[1])<20:
				pyautogui.click(button = 'left')

cap = cv2.VideoCapture(0)

print '**********************************************************************'
print '	You have entered calibration mode.'
print '	Defualt settings are visible on the trackbars.'
print ' Use the trackbars to calibrate and press SPACE when done.'
print '**********************************************************************'

#yellow_range = calibrateColor('Yellow', yellow_range)
#red_range = calibrateColor('Red', red_range)
#blue_range = calibrateColor('Blue', blue_range)

print '**********************************************************************'
print '	Press P to turn ON and OFF mouse simulation.'
print '	Press C to display the centroid of various colours.'
print '	Press ESC to exit.'
print '**********************************************************************'

while(1):

	k = cv2.waitKey(10) & 0xFF
	changeStatus(k)


	_, frameinv = cap.read()
	# flip horizontaly to get mirror image in camera
	frame = cv2.flip( frameinv, 1)

	hsv = cv2.cvtColor( frame, cv2.COLOR_BGR2HSV)

	b_mask = makeMask( hsv, blue_range)
	r_mask = makeMask( hsv, red_range)
	y_mask = makeMask( hsv, yellow_range)

	py_pos = y_pos 

	b_cen = drawCentroid( frame, b_area, b_mask, showCentroid)
	r_cen = drawCentroid( frame, r_area, r_mask, showCentroid)	
	y_cen = drawCentroid( frame, y_area, y_mask, showCentroid)
	
	if 	py_pos[0]!=-1 and y_cen[0]!=-1:
		y_pos = setCursorPos(y_cen, py_pos)
		print frame[GetSystemMetrics(0),GetSystemMetrics(1)]

	performAction(y_pos, r_cen, b_cen, perform)		
		
	cv2.imshow('Frame', frame)

	if k == 27:
		break

cv2.destroyAllWindows()
	
		


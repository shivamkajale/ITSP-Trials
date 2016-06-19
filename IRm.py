import cv2
import numpy as np
import pyautogui
import time

# Rectangular kernal for eroding and dilating the mask for primary noise removal 
kernel = np.ones((7,7),np.uint8)

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


def makeMask(hsv_frame, color_Range):
	
	mask = cv2.inRange( hsv_frame, color_Range[0], color_Range[1])
	# Morphosis next ...
	#eroded = cv2.erode( mask, kernel, iterations=1)
	#dilated = cv2.dilate( eroded, kernel, iterations=1)
	
	return mask

#red_range = np.array([[158,85,72],[180 ,255,255]])



cap=cv2.VideoCapture(0)

cv2.namedWindow('Parameters')
cv2.createTrackbar('Hue','Parameters',0,180,nothing)
cv2.createTrackbar('Sat','Parameters',0,255,nothing)
cv2.createTrackbar('Val',"Parameters",0,255,nothing)

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()
while(1):
	ret, frameinv=cap.read()
	frame=cv2.flip(frameinv,1)
	frame_hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

	h=cv2.getTrackbarPos('Hue','Parameters')
	s=cv2.getTrackbarPos('Sat','Parameters')
	v=cv2.getTrackbarPos('Val','Parameters')

	lwr=np.array([h-20,s,v])
	upr=np.array([h+20,255,255])

	red_range=np.array([lwr,upr])

	red_mask=makeMask(frame_hsv,red_range)

	cv2.imshow('red_mask',red_mask)

	

	
 
	# Change thresholds
	params.minThreshold = 10;
	params.maxThreshold = 200;
 
	# Filter by Area.
	params.filterByArea = True
	params.minArea = 75

	params.filterByColor=True
	params.blobColor=255

	# Set up the detector with default parameters.
	detector = cv2.SimpleBlobDetector_create(params)
 
	# Detect blobs.
	keypoints = detector.detect(red_mask)

	# Draw detected blobs as red circles.
	# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
	frame_with_keypoints = cv2.drawKeypoints(red_mask, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


	# Show keypoints

	cv2.imshow("Keypoints", frame_with_keypoints)

	k=cv2.waitKey(1)	&0xFF
	if k==27:
		break

	

'''
	mask=cv2.inRange(hsv,lwr,upr)
	_, contour, _=cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	area=np.zeros([len(contour)])
'''

cv2.destroyAllWindows()
cap.release()

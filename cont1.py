import numpy as np
import cv2

cap = cv2.VideoCapture(0)
while(1):
 	_, vidinv = cap.read()
 	vid = cv2.flip( vidinv, 1)

 	vid_gray = cv2.cvtColor( vid, cv2.COLOR_BGR2GRAY)

# 	mask = cv2.inRange( vid_hsv, np.array([161,123,133]), np.array([200,255,255])
# 	vid_gray = cv2.bitwise_and( vid.copy(), vid.copy(), mask = mask)

 	_, thresh = cv2.threshold( vid_gray, 20, 255, 0)
 	_, contour, _ = cv2.findContours( thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

 	vidCont = cv2.drawContours( vid, contour, -1, (0,0,255), 2)

 	cv2.imshow("Gray", vid_gray)
 	cv2.imshow("Contours", vidCont)

	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break

cv2.destroyAllWindows()
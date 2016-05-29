import numpy as np
import cv2

img = cv2.imread("intel.png")
s = img.shape

cv2.imshow("Intel", img)

img_gray = cv2.cvtColor(img.copy(),cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold( img_gray, 20, 255, 0)

image, contour, hie = cv2.findContours( thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

back = np.zeros( s, np.uint8)

ContourOnly = cv2.drawContours( back, contour, -1, (0,0,255), 1)
final = cv2.drawContours( img, contour, -1, (0,0,255), 1)

cv2.imshow("ContourOnly", ContourOnly)
cv2.imshow("Final", final)

cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()
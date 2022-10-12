import cv2
import numpy as np

path = ''
img = cv2.imread(path)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_range = np.array([110,50,50])
upper_range = np.array([130,255,255])

mask = cv2.inRange(hsv, lower_range, upper_range)

x, y, z = np.where(img==(255,255,255))
points =zip(x,y)
print(points)

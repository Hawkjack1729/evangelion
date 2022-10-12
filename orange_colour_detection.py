import cv2
import numpy as np

path=''
img = cv2.imread(path)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv,(10, 100, 20), (25, 255, 255) )

x, y, z = np.where(img==(255,255,255))
points =zip(x,y)
print(points)

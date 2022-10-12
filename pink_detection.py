import cv2
import numpy as np

img = cv2.imread('/home/ubuntu/Desktop/grid.png')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv,(85, 100, 20), (95, 255, 255) )

x, y, z = np.where(img==(255,255,255))
points =zip(x,y)
print(points)

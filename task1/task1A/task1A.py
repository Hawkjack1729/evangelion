'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 1A of Pharma Bot (PB) Theme (eYRC 2022-23).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_1a.py
# Functions:		detect_traffic_signals, detect_horizontal_roads_under_construction, detect_vertical_roads_under_construction,
#					detect_medicine_packages, detect_arena_parameters
# 					[ Comma separated list of functions in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
from cmath import pi
import re
import cv2
import numpy as np
from pyscreeze import pixel
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################
def nodes(l):
    X = {100:'A',200:'B',300:'C',400:'D',500:'E',600:'F',700:'G'}
    Y = {100:'1',200:'2',300:'3',400:'4',500:'5',600:'6',700:'7'}
    node = str(X[l[0]]) + str(Y[l[1]])
    return node
def get_color(x, y, maze_image):
    hsv = cv2.cvtColor(maze_image, cv2.COLOR_BGR2HSV)
    pixel_center = hsv[y, x]
    if pixel_center[0] == 15:
        return 'Orange'
    elif pixel_center[0] == 90:
        return 'Skyblue'
    elif pixel_center[0] == 60:
        return 'Green'
    elif pixel_center[0] == 159:
        return 'Pink'
def get_shop_number(x, y):
    if 100 < x < 200 and 100 < y < 200:
        return 'Shop_1'
    elif 200 < x < 300 and 100 < y < 200:
        return 'Shop_2'
    elif 300 < x < 400 and 100 < y < 200:
        return 'Shop_3'
    elif 400 < x < 500 and 100 < y < 200:
        return 'Shop_4'
    elif 500 < x < 600 and 100 < y < 200:
        return 'Shop_5'
    elif 600 < x < 700 and 100 < y < 200:
        return 'Shop_6'
##############################################################

def detect_traffic_signals(maze_image):

	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list of
	nodes in which traffic signals are present in the image

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`traffic_signals` : [ list ]
			list containing nodes in which traffic signals are present
	
	Example call:
	---
	traffic_signals = detect_traffic_signals(maze_image)
	"""    
	traffic_signals = []

	##############	ADD YOUR CODE HERE	##############
	mask = np.zeros(maze_image.shape, dtype=np.uint8)
	red_lower = np.array([0, 50, 50])
	red_upper = np.array([10, 255, 255])
	l1 = []
	hsv = cv2.cvtColor(maze_image,cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv,red_lower,red_upper)
	ret, thresh = cv2.threshold(mask.copy(), 10, 255, cv2.THRESH_BINARY)
	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	for contour in contours:
		M = cv2.moments(contour)
		l2 = []
		if M["m00"] != 0:
			x = int(M["m10"] / M["m00"])
			y = int(M["m01"] / M["m00"])
			if y % 100 == 0:
				l2.append(x)
				l2.append(y)
				l1.append(l2)
		else:
			x, y = 0, 0
	l1.sort()
	for i in l1:
		traffic_signals.append(nodes(i))
	##################################################
	
	return traffic_signals
	

def detect_horizontal_roads_under_construction(maze_image):
	
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list
	containing the missing horizontal links

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`horizontal_roads_under_construction` : [ list ]
			list containing missing horizontal links
	
	Example call:
	---
	horizontal_roads_under_construction = detect_horizontal_roads_under_construction(maze_image)
	"""    
	horizontal_roads_under_construction = []

	##############	ADD YOUR CODE HERE	##############
	horizontal_road = {}
	horizontal_road_total = [700,600,500,400,300,200,100]
	gray=cv2.cvtColor(maze_image,cv2.COLOR_BGR2GRAY)
	ret, thresh = cv2.threshold(gray.copy(), 10, 255, cv2.THRESH_BINARY)
	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	for contour in contours:
		M = cv2.moments(contour)
		if M["m00"] != 0:
			x = int(M["m10"] / M["m00"])
			y = int(M["m01"] / M["m00"])
			if x >= 80 and y >= 80:
				if x % 100 != 0 and x % 50 == 0:
					if x not in horizontal_road:
						horizontal_road.update({x: [y]})
					else:
						horizontal_road[x].append(y)
		else:
			x, y = 0, 0
	for key,value in horizontal_road.items():
		for i in horizontal_road_total:
			if i not in value:
				pre =str(nodes([int(key)-50,i]))
				post = str(nodes([int(key)+50,i]))
				horizontal_roads_under_construction.append(pre+'-'+post)
	horizontal_roads_under_construction.sort()
	##################################################

	return horizontal_roads_under_construction

def detect_vertical_roads_under_construction(maze_image):

	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list
	containing the missing vertical links

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`vertical_roads_under_construction` : [ list ]
			list containing missing vertical links
	
	Example call:
	---
	vertical_roads_under_construction = detect_vertical_roads_under_construction(maze_image)
	"""    
	vertical_roads_under_construction = []

	##############	ADD YOUR CODE HERE	##############
	vertical_road = {}
	vertical_road_total = [650,550,450,350,250,150]
	gray=cv2.cvtColor(maze_image,cv2.COLOR_BGR2GRAY)
	ret, thresh = cv2.threshold(gray.copy(), 10, 255, cv2.THRESH_BINARY)
	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	for contour in contours:
		M = cv2.moments(contour)
		if M["m00"] != 0:
			x = int(M["m10"] / M["m00"])
			y = int(M["m01"] / M["m00"])
			if x >= 80 and y >= 80:
				if x % 100 == 0:
					if x not in vertical_road:
						vertical_road.update({x: [y]})
					else:
						vertical_road[x].append(y)
		else:
			x, y = 0, 0
	for key,value in vertical_road.items():
		for i in vertical_road_total:
			if i not in value:
				pre =str(nodes([int(key),int(i)-50]))
				post = str(nodes([int(key),int(i)+50]))
				vertical_roads_under_construction.append(pre+'-'+post)
	vertical_roads_under_construction.sort()
	##################################################
	
	return vertical_roads_under_construction


def detect_medicine_packages(maze_image):

	"""
	Purpose:
	---
	This function takes the image as an argument and returns a nested list of
	details of the medicine packages placed in different shops

	** Please note that the shop packages should be sorted in the ASCENDING order of shop numbers 
	   as well as in the alphabetical order of colors.
	   For example, the list should first have the packages of shop_1 listed. 
	   For the shop_1 packages, the packages should be sorted in the alphabetical order of color ie Green, Orange, Pink and Skyblue.

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`medicine_packages` : [ list ]
			nested list containing details of the medicine packages present.
			Each element of this list will contain 
			- Shop number as Shop_n
			- Color of the package as a string
			- Shape of the package as a string
			- Centroid co-ordinates of the package
	Example call:
	---
	medicine_packages = detect_medicine_packages(maze_image)
	"""    
	medicine_packages_present = []

	##############	ADD YOUR CODE HERE	##############
	hsv = cv2.cvtColor(maze_image, cv2.COLOR_BGR2HSV)
	mask = np.zeros(maze_image.shape, dtype=np.uint8)
	mask1 = np.zeros(maze_image.shape, dtype=np.uint8)
	mask2 = np.zeros(maze_image.shape, dtype=np.uint8)
	skyblue_lower = np.array([85, 100, 20])
	skyblue_upper = np.array([95, 255, 255])
	orange_lower = np.array([5, 100, 20])
	orange_upper = np.array([25, 255, 255])
	pink_lower = np.array([149, 100, 100])
	pink_upper = np.array([169, 255, 255])
	green_lower = np.array([50, 100, 20])
	green_upper = np.array([70, 255, 255])
	mask_skyblue = cv2.inRange(hsv, skyblue_lower, skyblue_upper)
	mask_green = cv2.inRange(hsv, green_lower, green_upper)
	mask_pink = cv2.inRange(hsv, pink_lower, pink_upper)
	mask_orange = cv2.inRange(hsv, orange_lower, orange_upper)
	mask1 = cv2.bitwise_or(mask_skyblue, mask_green, mask1)
	mask2 = cv2.bitwise_or(mask1, mask_pink, mask2)
	mask = cv2.bitwise_or(mask2, mask_orange, mask)
	ret, thresh = cv2.threshold(mask.copy(), 10, 255, cv2.THRESH_BINARY)
	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	for contour in contours:
		M = cv2.moments(contour)
		approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
		l1 = []
		if M["m00"] != 0:
			x = int(M["m10"] / M["m00"])
			y = int(M["m01"] / M["m00"])
			if x != 100:
				if len(approx) == 3:
					l2 = [x, y]
					l1.append(get_shop_number(x, y))
					l1.append(get_color(x, y, maze_image))
					l1.append('Triangle')
					l1.append(l2)
					medicine_packages_present.append(l1)
				elif len(approx) == 4:
					l2 = [x, y]
					l1.append(get_shop_number(x, y))
					l1.append(get_color(x, y, maze_image))
					l1.append('Square')
					l1.append(l2)
					# l1.append(y)
					medicine_packages_present.append(l1)
				else:
					l2 = [x, y]
					l1.append(get_shop_number(x, y))
					l1.append(get_color(x, y, maze_image))
					l1.append('Circle')
					l1.append(l2)
					# l1.append(y)
					medicine_packages_present.append(l1)
		else:
			x, y = 0, 0
	medicine_packages_present.sort()
	##################################################

	return medicine_packages_present

def detect_arena_parameters(maze_image):

	"""
	Purpose:
	---
	This function takes the image as an argument and returns a dictionary
	containing the details of the different arena parameters in that image

	The arena parameters are of four categories:
	i) traffic_signals : list of nodes having a traffic signal
	ii) horizontal_roads_under_construction : list of missing horizontal links
	iii) vertical_roads_under_construction : list of missing vertical links
	iv) medicine_packages : list containing details of medicine packages

	These four categories constitute the four keys of the dictionary

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`arena_parameters` : { dictionary }
			dictionary containing details of the arena parameters
	
	Example call:
	---
	arena_parameters = detect_arena_parameters(maze_image)
	"""    
	arena_parameters = {}

	##############	ADD YOUR CODE HERE	##############
	arena = {'traffic_signals':detect_traffic_signals(maze_image),
          'horizontal_roads_under_construction':detect_horizontal_roads_under_construction(maze_image),
          'vertical_roads_under_construction':detect_vertical_roads_under_construction(maze_image),
          'medicine_packages_present':detect_medicine_packages(maze_image)
          }
	arena_parameters.update(arena)
	##################################################
	
	return arena_parameters

######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS FUNCTION #########	

if __name__ == "__main__":

    # path directory of images in test_images folder
	img_dir_path = "public_test_images/"

    # path to 'maze_0.png' image file
	file_num = 0
	img_file_path = img_dir_path + 'maze_' + str(file_num) + '.png'
	
	# read image using opencv
	maze_image = cv2.imread(img_file_path)
	
	print('\n============================================')
	print('\nFor maze_' + str(file_num) + '.png')

	# detect and print the arena parameters from the image
	arena_parameters = detect_arena_parameters(maze_image)

	print("Arena Prameters: " , arena_parameters)

	# display the maze image
	cv2.imshow("image", maze_image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	choice = input('\nDo you want to run your script on all test images ? => "y" or "n": ')
	
	if choice == 'y':

		for file_num in range(1, 15):
			
			# path to maze image file
			img_file_path = img_dir_path + 'maze_' + str(file_num) + '.png'
			
			# read image using opencv
			maze_image = cv2.imread(img_file_path)
	
			print('\n============================================')
			print('\nFor maze_' + str(file_num) + '.png')
			
			# detect and print the arena parameters from the image
			arena_parameters = detect_arena_parameters(maze_image)

			print("Arena Parameter: ", arena_parameters)
				
			# display the test image
			cv2.imshow("image", maze_image)
			cv2.waitKey(2000)
			cv2.destroyAllWindows()

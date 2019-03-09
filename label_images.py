import cv2
import os
import sys
import numpy as np
import getch
import imutils

image_directory = sys.argv[1]

curr_img = None

points = []
pointsList = []

def click_and_crop(event, x, y, flags, param):
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	global curr_img
	global points
	if event == cv2.EVENT_LBUTTONDOWN:
		points.append((x, y))
		points_len = len(points)
		font = font = cv2.FONT_HERSHEY_SIMPLEX
		if (points_len == 1):
			cv2.circle(curr_img, (x, y), 10, (0, 255, 0))
			cv2.putText(curr_img, 'TopLeft', (x + 2, y + 2), font, 1, (255, 0, 0), 2)
			cv2.imshow('image', curr_img)
		elif(points_len == 2):
			cv2.circle(curr_img, (x, y), 10, (0, 255, 0))
			cv2.putText(curr_img, 'TopRight', (x + 2, y + 2), font, 1, (255, 0, 0), 2)
			cv2.line(curr_img, points[0], points[1], (0,255,0), 2)
			cv2.imshow('image', curr_img)
		elif(points_len == 3):
			cv2.circle(curr_img, (x, y), 10, (0, 255, 0))
			cv2.putText(curr_img, 'BottomLeft', (x + 2, y + 2), font, 1, (255, 0, 0), 2)
			cv2.line(curr_img, points[0], points[2], (0,255,0), 2)
			cv2.imshow('image', curr_img)
		elif(points_len == 4):
			cv2.circle(curr_img, (x, y), 10, (0, 255, 0))
			cv2.putText(curr_img, 'BottomRight', (x + 2, y + 2), font, 1, (255, 0, 0), 2)
			cv2.line(curr_img, points[1], points[3], (0,255,0), 2)
			cv2.line(curr_img, points[2], points[3], (0,255,0), 2)
			cv2.imshow('image', curr_img)
		else:
			print('Already drew 4 points!')

def drawCurrPoints(curr_img, pointsList):
	for points in pointsList:
		cv2.circle(curr_img, points[0], 10, (0, 255, 255))
		cv2.circle(curr_img, points[1], 10, (0, 255, 255))
		cv2.circle(curr_img, points[2], 10, (0, 255, 255))
		cv2.circle(curr_img, points[3], 10, (0, 255, 255))
		cv2.line(curr_img, points[0], points[1], (0,0,255), 2)
		cv2.line(curr_img, points[0], points[2], (0,0,255), 2)
		cv2.line(curr_img, points[1], points[3], (0,0,255), 2)
		cv2.line(curr_img, points[2], points[3], (0,0,255), 2)

def main():
	global curr_img
	global points
	global pointsList
	cv2.namedWindow("image")
	cv2.setMouseCallback("image", click_and_crop)
	filenames = os.listdir(image_directory)
	print(filenames)
	i = 0
	while(i < len(filenames)):
		filename = os.path.join(image_directory, filenames[i])
		curr_img = cv2.imread(filename)
		if (not(curr_img is None)):
			print(filename)
			curr_img_copy = curr_img.copy()
			curr_img = imutils.resize(curr_img, width = 500)
			drawCurrPoints(curr_img, pointsList)
			cv2.imshow('image', curr_img)

			key = cv2.waitKey(0)

			if (key == ord("r")):
				print('Resetting image, including all already labeled hoops')
				points = []
				curr_img = curr_img_copy
				curr_img = imutils.resize(curr_img, width = 500)
			elif(key == ord("s")):
				print('Saving Points')
				# Saving points
				j = 0
				if (not((len(points) % 4) == 0)):
					print('Invalid number of points')
					curr_img = curr_img_copy
					curr_img = imutils.resize(curr_img, width = 500)
				else:
					pointsList.append(points)
					with open(filename + '.txt', "w+") as out_file:
						(oldwidth, oldh, oldc) = curr_img.shape
						(newwidth, newh, newc) = curr_img_copy.shape
						ratio = (newwidth / oldwidth)
						for thesePoints in pointsList:
							j = 0
							while (j < 4):
								thesePoints[j] = tuple(int(ratio * x) for x in points[j])
								out_file.write(str(thesePoints[j]))
								j = j + 1
							out_file.write('\n')
					i = i + 1
					pointsList = []
				points = []
			elif (key == ord("n")):
				if (not((len(points) % 4) == 0)):
					print('Invalid number of points')
					curr_img = curr_img_copy
					curr_img = imutils.resize(curr_img, width = 500)
				else:
					pointsList.append(points)
					print('You can now label another hoop')
				points = []
			else:
				print('Invalid key press')
		else:
			i = i + 1
		
if __name__== "__main__":
	main()

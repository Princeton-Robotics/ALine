import cv2
import os
import sys
import numpy as np

image_directory = sys.argv[1]

curr_img = None

points = []

def click_and_crop(event, x, y, flags, param):
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	if event == cv2.EVENT_LBUTTONDOWN:
		points.append((x, y))
        points_len = len(points)
        font = font = cv2.FONT_HERSHEY_SIMPLEX
        if (points_len == 1):
            cv2.circle(curr_img, (x, y), 2, (0, 255, 0))
            cv2.putText(curr_img, 'TopLeft', (x + 2, y + 2), font, 1, (255, 0, 0), 2)
            cv2.imshow('image', curr_img)
        elif(points_len == 2):
            cv2.circle(curr_img, (x, y), 2, (0, 255, 0))
            cv2.putText(curr_img, 'TopRight', (x + 2, y + 2), font, 1, (255, 0, 0), 2)
            cv2.line(curr_img, points[0], points[1], (0,255,0), 2)
            cv2.imshow('image', curr_img)
        elif(points_len == 3):
            cv2.circle(curr_img, (x, y), 2, (0, 255, 0))
            cv2.putText(curr_img, 'BottomLeft', (x + 2, y + 2), font, 1, (255, 0, 0), 2)
            cv2.line(curr_img, points[0], points[2], (0,255,0), 2)
            cv2.imshow('image', curr_img)
        elif(points_len == 4):
            cv2.circle(curr_img, (x, y), 2, (0, 255, 0))
            cv2.putText(curr_img, 'BottomRight', (x + 2, y + 2), font, 1, (255, 0, 0), 2)
            cv2.line(curr_img, points[1], points[3], (0,255,0), 2)
            cv2.imshow('image', curr_img)
        else:
            print('Already drew 4 points!')

def main():
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_and_crop)
    filenames = os.listdir(image_directory)
    i = 0

    while(i < len(filenames)):
        filename = filenames[i]
        curr_img = cv2.imread(filename)
        curr_img_copy = curr_img.copy()
        (width, height, channels) = cv2.GetSize(curr_img)
        cv2.imshow('image', curr_img)

        key = cv2.waitKey(1) & 0xFF

        if (key == ord("r")):
            print('Resetting image')
            points = []
            curr_img = curr_img_copy
        elif(key == ord("s")):
            print('Saving Points')
            # Saving points
            j = 0
            with open(filename + '.txt', "w+") as out_file:
                while (j < 4):
                    out_file.write(str(points[j]), file=out_file)
                    j = j + 1
            points = []
            i = i + 1
        else:
            print('Invalid key press')
        

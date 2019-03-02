"""
Demo of the Mambo vision using DroneVisionGUI that relies on libVLC and shows how to make a
second window using opencv to draw on the processed window.  It is a different
multi-threaded approach than DroneVision
Author: Amy McGovern
"""
from pyparrot.Bebop import Bebop
from pyparrot.DroneVisionGUI import DroneVisionGUI
import cv2
import time

import numpy as np
from matplotlib import pyplot as plt
import imutils as im
import math


# set this to true if you want to fly for the demo
testFlying = False
font = cv2.FONT_HERSHEY_SIMPLEX

def draw_second_pictures(args):
	"""
	Grab the latest stream from the drone and draw it in a second opencv window with some text to show that it
	is being processed
	:param args:
	:return:
	"""

	# get the vision
	mamboVision = args[0]

	# get the latest images
	img = mamboVision.get_latest_valid_picture()

	# if the images is invalid, return
	if(img is None):
		return

	# put the roll and pitch at the top of the screen
	# cv2.putText(img, 'demo text', (50, 50), font, 1, (255, 0, 255), 2, cv2.LINE_AA)
	# cv2.imshow("MarkerStream", img)
	#cv2.waitKey(1000)

	kernal = np.array((
		[-1,-1,-1],
		[-1,8,-1],
		[-1,-1,-1]
	))

	toFilter = img[:,:,2] - img[:,:,1] - img[:,:,0]

	lines = cv2.filter2D(toFilter, -1, kernal)

	th, dst = cv2.threshold(lines, 100, 255, cv2.THRESH_BINARY)

	lines = cv2.HoughLines(dst, 1,np.pi/180 , 70)

	ret,thresh1 = cv2.threshold(toFilter, 75,255, cv2.THRESH_BINARY_INV)

	#cv2.imshow('dst',dst)

	#if (lines == None):
		#print("no line found")
	#else: 

	#height: 480 width: 856

	height, width, channels = img.shape
	centerX = width/2
	centerY = height/2

	theta_error_prior = 0
	theta_integral = 0
	theta_KP = 1
	theta_KI = 0
	theta_KD = 0
	bias = 0
	rho_sign = 0

	desired_value = 0
	iteration_time = 1

	if (lines is None):
		print("no line found")
	else:
		for rho, theta in lines[0]:
			a = np.cos(theta)
			b = np.sin(theta)
			x0 = a*rho
			y0 = b*rho
			x1 = int(x0 + 1000*(-b))
			y1 = int(y0 + 1000*(a))
			x2 = int(x0 - 1000*(-b))
			y2 = int(y0 - 1000*(a))

			cv2.line(img,(x1,y1),(x2,y2),(255,0,0),2)
			cv2.putText(img, 'r: ' + str(rho), (50,50), font, 1, (255, 0, 255), 2, cv2.LINE_AA)
			cv2.putText(img, 'theta: ' + str(theta), (50,75), font, 1, (255,0,255), 2, cv2.LINE_AA)
			
			# theta_error = desired_value - theta
			rho_sign = rho / abs(rho)
			#want theta_error to be negative when drone is facing right of desired path.
			#yaw goes from -100 to 100. 100 goes clkwise.
			# if(rho_sign < 0):
			# 	theta_error = desired_value - (math.pi + theta)
			# else:
			# 	theta_error = desired_value - theta
			# if(rho_sign < 0):
			# 	theta = (math.pi - theta)
			# else:
			# 	theta = -1 * theta

			if(abs(x1-x2) > 5):
				slope = ((y2 - y1)/(x2-x1))/abs((y2 - y1)/(x2-x1))
			else:
				slope =1

			if(slope < 0):
				theta = -1 * (theta)
			else:
				theta = math.pi - theta

			theta_error = desired_value - theta

			theta_integral = theta_integral + (theta_error*iteration_time)
			theta_derivative = (theta_error - theta_error_prior)/iteration_time
			theta_output = theta_KP*theta_error + theta_KI*theta_integral + theta_KD*theta_derivative + bias
			theta_error_prior = theta_error
			theta_output = int(25*theta_output)

			cv2.putText(img, 'theta output: ' + str(theta_output), (50,100), font, 1, (255,0,255), 2, cv2.LINE_AA)

				#finds red things and makes them white

	#trying to crop and then analyze
	# thresh2 = thresh1[int(y0)-50:int(y0)+50, int(x0)-50:int(x0)+50]
	M = cv2.moments(thresh1)

	if(M["m00"] != 0):
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
	else:
		cX =0
		cY =0
	cv2.circle(img, (cX, cY), 5, (0, 0, 255), -1)
	cv2.imshow('thresh1', thresh1)
	"""
	MAKE SURE TO UNCOMMENT THIS WHEN FLYING!!!!!!!!!!!!!!!!!!!!!!!
	"""
	# mambo.fly_direct(roll=0, pitch=0, yaw=25*theta_output, vertical_movement=0, duration=iteration_time)

	cv2.imshow('houghlines3.jpg', img)
	cv2.waitKey(100)
	
def demo_mambo_user_vision_function(mamboVision, args):
	"""
	Demo the user code to run with the run button for a mambo
	:param args:
	:return:
	"""
	mambo = args[0]

	if (testFlying):
	# 	print("taking off!")
	# 	mambo.safe_takeoff(5)

		# if (mambo.sensors.flying_state != "emergency"):
		# 	print("flying state is %s" % mambo.sensors.flying_state)
		# 	print("Flying direct: going up")
		# 	mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=15, duration=2)

		# 	print("flip left")
		# 	print("flying state is %s" % mambo.sensors.flying_state)
		# 	success = mambo.flip(direction="left")
		# 	print("mambo flip result %s" % success)
		# 	mambo.smart_sleep(5)

		print("landing")
		print("flying state is %s" % mambo.sensors.flying_state)
		mambo.safe_land(5)
	else:
		print("Sleeeping for 15 seconds - move the mambo around")
		mambo.smart_sleep(15)

	# done doing vision demo
	print("Ending the sleep and vision")
	mamboVision.close_video()

	mambo.smart_sleep(5)

	print("disconnecting")
	mambo.disconnect()

if __name__ == "__main__":
	# make my mambo object
	# remember to set True/False for the wifi depending on if you are using the wifi or the BLE to connect
	# the address can be empty if you are using wifi
	mambo = Bebop()
	print("trying to connect to mambo now")

	success = mambo.connect(num_retries=3)
	print("connected: %s" % success)
	mambo.pan_tilt_camera_velocity(-90,0,1)

	if (success):
		# get the state information
		print("sleeping")
		mambo.smart_sleep(1)
		mambo.ask_for_state_update()
		mambo.smart_sleep(1)
		# setup the extra window to draw the markers in
		cv2.namedWindow("ExampleWindow")
		cv2.namedWindow("dst")


		print("Preparing to open vision")
		mambo.pan_tilt_camera_velocity(-90,0,1)
		mamboVision = DroneVisionGUI(mambo, is_bebop=True, buffer_size=200,
									 user_code_to_run=demo_mambo_user_vision_function, user_args=(mambo, ))

		mamboVision.set_user_callback_function(draw_second_pictures, user_callback_args=(mamboVision, ))
		mamboVision.open_video()
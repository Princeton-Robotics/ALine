from pyparrot.Bebop import Bebop
import cv2

bebop = Bebop()

print("connecting")
success = bebop.connect(10)
print(success)

try:
	print("sleeping")
	bebop.smart_sleep(5)
	
	bebop.ask_for_state_update()

	# bebop.safe_takeoff(10)

	# bebop.set_max_rotation_speed(200)
	
	# bebop.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=90, duration=1)
	
	bebop.smart_sleep(1)

	print('Opening stream')
	bebop.start_video_stream()

	cam = cv2.VideoCapture("./bebop.sdp")

	while True:
		ret, frame = cam.read()
		cv2.imshow("frame",frame)
		cv2.waitKey(1)
	#print('Opening with opencv')
	#stream = cv2.VideoCapture("bebop.sdp")
	print('done, wait 10 seconds')
	bebop.smart_sleep(5)
	#bebop.smart_sleep(1000)
	
	
	#bebop.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=-75, duration=1)
	
	#bebop.smart_sleep(1)
	
	# bebop.fly_direct(roll=0, pitch=0, yaw=100, vertical_movement=0, duration=5)
	# bebop.flip(direction="front")
	bebop.smart_sleep(1)
	# bebop.flip(direction="right")
	# bebop.smart_sleep(1)
	# bebop.flip(direction="front")
	# bebop.smart_sleep(1)
	# bebop.flip(direction="back")
	# bebop.smart_sleep(1)
	print("trying to read from stream")
	#(grabbed, frame) = stream.read()
	#cv2.imshow("Face Detection", frame)
except Exception as e:
	print('error')
	print(e)

bebop.safe_land(10)

bebop.stop_video_stream()

bebop.disconnect()

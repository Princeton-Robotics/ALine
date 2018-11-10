from pyparrot.Bebop import Bebop

bebop = Bebop()

print("connecting")
success = bebop.connect(10)
print(success)

bebop.start_video_stream()
bebop.smart_sleep(2)
bebop.safe_takeoff(10)
bebop.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=30, duration=2)



bebop.safe_land(10)

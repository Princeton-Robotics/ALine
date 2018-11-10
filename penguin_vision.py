from pyparrot.Bebop import Bebop

bebop = Bebop()

print("connecting")
success = bebop.connect(10)
print(success)

bebopVision = DroneVision(bebop, is_bebop=True)

bebop.start_video_stream()
bebop.smart_sleep(10)
viewVideo = bebopVision.open_video()
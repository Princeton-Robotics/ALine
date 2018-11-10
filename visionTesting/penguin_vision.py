from pyparrot.Bebop import Bebop

bebop = Bebop()

print("connecting")
success = bebop.connect(10)
print(success)

bebop.start_video_stream()
bebop.smart_sleep(10)
from pyparrot.Bebop import Bebop
from pyparrot.DroneVisionGUI import DroneVisionGUI

class UserVision:
    def __init__(self, vision):
        self.index = 0
        self.vision = vision

    def save_pictures(self, args):
        #print("saving picture")
        img = self.vision.get_latest_valid_picture()

        if (img is not None):
            filename = "test_image_%06d.png" % self.index
            #cv2.imwrite(filename, img)
            self.index += 1

def helloworld(bebopVision, args):
    print("Hi chuck!")
    return

if __name__ == "__main__":
    bebop = Bebop()
    connected = bebop.connect(5)

    if (connected):
        bebopVision = DroneVisionGUI(bebop, is_bebop = True, user_code_to_run=helloworld, user_args=None)
        userVision = UserVision(bebopVision)
        bebopVision.set_user_callback_function(userVision.save_pictures, user_callback_args=None)
        bebopVision.open_video()
    else:
        print("failed")
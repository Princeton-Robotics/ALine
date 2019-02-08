"""
Demo of the Bebop vision using DroneVisionGUI (relies on libVLC).  It is a different
multi-threaded approach than DroneVision

Author: Amy McGovern
"""
from pyparrot.Bebop import Bebop
from pyparrot.DroneVisionGUI import DroneVisionGUI
import threading
import cv2
import time
import numpy as np

isAlive = False

class UserVision:
    def __init__(self, vision):
        self.index = 0
        self.vision = vision

    def save_pictures(self, args):
        print("saving picture xxx")
        img = self.vision.get_latest_valid_picture()

        if (img is not None):
            filename = "saved_images/test_image_%06d.png" % self.index
            # cv2.imwrite(filename, img)

            kernal = np.array((
                [-1,2,-1],
                [-1,2,-1],
                [-1,2,-1]
            ))

            lines = cv2.filter2D(img[:,:,2], -1, kernal)

            th, dst = cv2.threshold(lines, 100, 255, cv2.THRESH_BINARY)

            lines = cv2.HoughLines(dst, 1, np.pi/180 , 70)

            if (lines is not None):
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

                cv2.imwrite(filename, img)
                cv2.waitKey(1000)

            self.index +=1

def demo_user_code_after_vision_opened(bebopVision, args):
    bebop = args[0]

    print("Vision successfully started!")
    print("Fly me around by hand!")
    bebop.smart_sleep(15)

    if (bebopVision.vision_running):
        print("Moving the camera using velocity")
        bebop.pan_tilt_camera_velocity(pan_velocity=0, tilt_velocity=-2, duration=4)
        bebop.smart_sleep(0.2)

        # land
        bebop.safe_land(5)

        print("Finishing demo and stopping vision")
        bebopVision.close_video()

    # disconnect nicely so we don't need a reboot
    print("disconnecting")
    bebop.disconnect()

if __name__ == "__main__":
    # make my bebop object
    bebop = Bebop()

    # connect to the bebop
    success = bebop.connect(5)

    if (success):
        # start up the video
        bebopVision = DroneVisionGUI(bebop, is_bebop=True, user_code_to_run=demo_user_code_after_vision_opened,
                                     user_args=(bebop, ))

        userVision = UserVision(bebopVision)
        bebopVision.set_user_callback_function(userVision.save_pictures, user_callback_args=None)
        bebopVision.open_video()

    else:
        print("Error connecting to bebop.  Retry")


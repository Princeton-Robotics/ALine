from pyparrot.Bebop import Bebop
from pyparrot.DroneVisionGUI import DroneVisionGUI
import cv2
import time

import numpy as np
from matplotlib import pyplot as plt
import imutils as im

=======
import math
>>>>>>> d9e580835b781dae266caf135856e7e342d6feea


# set this to true if you want to fly for the demo
testFlying = False
font = cv2.FONT_HERSHEY_SIMPLEX

if __name__ == "__main__":
    # make my mambo object
    # remember to set True/False for the wifi depending on if you are using the wifi or the BLE to connect
    # the address can be empty if you are using wifi
    mambo = Bebop()
    print("trying to connect to mambo now")

    success = mambo.connect(num_retries=3)
    print("connected: %s" % success)

    mambo.safe_land(5)

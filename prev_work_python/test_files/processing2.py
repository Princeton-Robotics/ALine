import numpy as np
import cv2
from matplotlib import pyplot as plt
import imutils as im

import execjs

ctx = execjs.compile('''
var bebop = require("node-bebop/lib");
var drone = bebop.createClient();

function conn(){
  return drone.connect(function() {
    drone.MediaStreaming.videoStreamMode(2);
    drone.PictureSettings.videoStabilizationMode(3);
    drone.MediaStreaming.videoEnable(1);
  });
}
''')

print(ctx.call('conn'))

cam = cv2.VideoCapture("./bebop.sdp")
skip_frames = 10

while True:
    filename = "saved_images/test_image_111.png"
    ret, img = cam.read()
    cv2.imwrite(filename, img)
    cv2.waitKey(1)

    # Capture frame-by-frame
    img = im.resize(img, height=400)

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #edges = cv2.Canny(frame[:,:,2], 50, 150, apertureSize = 3, L2gradient = True)
    #cv2.imshow('HI',edges)
    #cv2.waitKey(1000)

    kernal = np.array((
                [-1,2,-1],
                [-1,2,-1],
                [-1,2,-1]
            ))

    lines = cv2.filter2D(img[:,:,2], -1, kernal)

    th, dst = cv2.threshold(lines, 100, 255, cv2.THRESH_BINARY)

    lines = cv2.HoughLines(dst, 1, np.pi/180 , 70)

    cv2.imwrite(filename, dst)
    cv2.waitKey(1000)

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

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
import numpy as np
import cv2
from matplotlib import pyplot as plt

cap = cv2.VideoCapture("LineExample.mp4")
skip_frames = 10

while(True):
    # Capture frame-by-frame
    for i in range(skip_frames):
        cap.grab()
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 75, 200, apertureSize = 3, L2gradient = True)
    lines = cv2.HoughLines(edges, 1,np.pi/180 , 70)

    for line in lines:
        for rho, theta in line:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))

            cv2.line(frame,(x1,y1),(x2,y2),(0,0,255),2)

    cv2.imwrite('houghlines3.jpg', frame)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
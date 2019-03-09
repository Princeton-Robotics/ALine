import numpy as np
import cv2
from matplotlib import pyplot as plt
import imutils as im

cap = cv2.VideoCapture("IMG_2002.mov")
skip_frames = 10

while(True):
    # Capture frame-by-frame
    for i in range(skip_frames):
        cap.grab()
    ret, frame = cap.read()
    frame = im.resize(frame, height=400)

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #edges = cv2.Canny(frame[:,:,2], 50, 150, apertureSize = 3, L2gradient = True)
    #cv2.imshow('HI',edges)
    #cv2.waitKey(1000)

    '''kernal = np.array((
        [-2,1,2,1,-2],
        [-2,1,2,1,-2],
        [-2,1,2,1,-2],
        [-2,1,2,1,-2],
        [-2,1,2,1,-2]
    ))'''

    kernal = np.array((
        [-1,-1,-1],
        [-1,8,-1],
        [-1,-1,-1]
    ))

    kernalDiagonal = np.array((
        [-1,-1,-1],
        [2,2,2],
        [-1,-1,-1]
    ))

    lines = cv2.filter2D(frame[:,:,2], -1, kernal)
    linesDiag = cv2.filter2D(frame[:,:,2], -1, kernalDiagonal)

    th, dst = cv2.threshold(lines, 100, 255, cv2.THRESH_BINARY)
    thDiag, dstDiag = cv2.threshold(linesDiag, 100, 255, cv2.THRESH_BINARY)

    dst = np.add(dst, dstDiag)

    lines = cv2.HoughLines(dst, 1,np.pi/180 , 70)

    cv2.imshow('dst',dst)
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

        cv2.line(frame,(x1,y1),(x2,y2),(255,0,0),2)

    cv2.imshow('houghlines3.jpg', frame)
    cv2.waitKey(1000)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
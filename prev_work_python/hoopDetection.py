import cv2
from sklearn.cluster import KMeans
import numpy as np
import imutils
import sys

# cap = cv2.VideoCapture(0)

while(1):
   # Take each frame
   # _, frame = cap.read()
   frame = cv2.imread(sys.argv[1])
   frame = imutils.resize(frame, width = 500)
   height, width, depth = frame.shape

   # Convert BGR to HSV
   hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
   h = hsv[:,:,0]

   # define range of blue color in HSV
   # lower_orange = np.array([5, 170, 100])
   # upper_orange = np.array([15, 255, 255])

   # Threshold the HSV image to get only blue colors
   #mask = cv2.inRange(h, 12, 15)
   h[h<5] = 0
   h[h>15] = 0
   h[h>=5] = 1

   # Bitwise-AND mask and original image
   res = h[:,:,np.newaxis] * frame
   cv2.imshow('h', h * 255)
   k = cv2.waitKey(10000)
   cv2.imshow('res', res)
   k = cv2.waitKey(10000)

   cnts, _ = cv2.findContours(h, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
   maxArea = 0
   maxContour = None
   for cnt in cnts:
      area = cv2.contourArea(cnt)
      if area > maxArea:
         maxArea = area
         maxContour = cnt
   blank = np.zeros((height, width , depth), np.uint8)
   cv2.drawContours(frame, maxContour, -1, (0, 255, 0), 3)
   cv2.drawContours(blank, maxContour, -1, (255, 255, 255), 3)
   # minRect = cv2.minAreaRect(maxContour)
   # minHull = cv2.convexHull(maxContour)
   # minDP = cv2.approxPolyDP(maxContour, 1, True)
   # cv2.drawContours(frame, minRect, -1, (0, 255, 0), 3)
   # cv2.drawContours(frame, minHull, -1, (255, 0, 0), 3)
   # cv2.drawContours(frame, minDP, -1, (0, 0, 255), 3)

   cv2.imshow('blank', blank)
   k = cv2.waitKey(10000)

   oldLines = cv2.HoughLines(blank[:,:,0], 1,np.pi/180 , 180)
   print(oldLines.shape)
   lines = []
   for line in oldLines:
      for rho, theta in line:
         a = np.cos(theta)
         b = np.sin(theta)
         x0 = a*rho
         y0 = b*rho
         x1 = int(x0 + 1000*(-b))
         y1 = int(y0 + 1000*(a))
         x2 = int(x0 - 1000*(-b))
         y2 = int(y0 - 1000*(a))
         lines.append([x1, y1, x2, y2])

   if lines is None:
      print("there are no lines")
      break

   for i in range(len(lines)):
      x1, y1, x2, y2 = lines[i]
      cv2.line(blank, (x1, y1), (x2, y2), (0,  0, 255), 2)

   cv2.imshow('blank', blank)
   k = cv2.waitKey(10000)

   points = []
   for i in range(len(lines)):
      x1, y1, x2, y2 = lines[i]
      for j in range(i + 1, len(lines)):
         x3, y3, x4, y4 = lines[j][0]
         m1 = (y2 - y1) / (x2 - x1 + 0.001)
         c1 = y1 - m1 * x1
         m3 = (y4 - y3) / (x4 - x3 + 0.001)
         c3 = y3 - m3 * x3
         if (abs(m1 - m3) < 0.001):
            continue
         x = (c3 - c1) / (m1 - m3 + 0.001)
         y = m1 * x + c1
         if x > 0 and x < width and y > 0 and y < height:
            points.append([x, y])

         cv2.circle(blank, (int(x), int(y)), 1, (0, 0, 255), -1)
      # for x1, y1, x2, y2 in line:
      #    points.append([x1, y1])
      #    points.append([x2, y2])
      #    cv2.line(blank, (x1,y1),(x2,y2),(0,0,255), 2)


   
   if not len(points) == 4:
      print("Not 4 points")
      break

   kmeans = KMeans(n_clusters=4, random_state=0).fit(points)
   print("CLUSTERS:", kmeans.cluster_centers_)
   for point in kmeans.cluster_centers_:
      cv2.circle(blank, (int(point[0]), int(point[1])), 5, (255, 0, 0), -1)

   # blank = cv2.cornerHarris(blank[:,:,0], 2, 3, 0.04)
   # blank = cv2.dilate(blank, None)

   cv2.imshow('h', h)
   cv2.imshow('frame', frame)
   cv2.imshow('res', res)
   cv2.imshow('blank', blank)
   k = cv2.waitKey(1)
   if k == 27:
      break

cv2.destroyAllWindows()

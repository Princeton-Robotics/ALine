import cv2
import imutils
from matplotlib import pyplot as plt
import numpy as np

orb = cv2.ORB_create()
FLANN_INDEX_LSH = 6

def match_features_orb(im1, im2):
    kpA, desA = orb.detectAndCompute(im1, None)
    kpB, desB = orb.detectAndCompute(im2, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)
    matches = bf.match(desA, desB)
    goodKeyPointsA = []
    goodKeyPointsB = []
    print(matches)
    for i, match in enumerate(matches):
        '''
        if len(match) < 2:
            print(i, "could not unpack error")
            continue
        m, n = match
        '''
        if matches[i].distance < 45: # * matches[i][1].distance: # Aparently determined in some paper to work well
            goodMatch = match
            goodKeyPointsA.append(kpA[goodMatch.queryIdx])
            goodKeyPointsB.append(kpB[goodMatch.trainIdx])

    return goodKeyPointsA, goodKeyPointsB

def match_features_orb_desc(kpA, desA, im2):
    kpB, desB = orb.detectAndCompute(im2, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)
    matches = bf.match(desA,desB)
    # print(matches[0])
    for i,(m,n) in enumerate(matches):
        if m.distance >= 0.7 *n.distance: # Aparently determined in some paper to work well
            matches[i] = 'Apple'
    matches[:] = [match for match in matches if match != 'Apple']
    
    return kpA, kpB, desA, desB, matches

def find_keypoints(im):
    if (im.shape[2] > 1):
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    a = cv2.cornerHarris(im, 3, 3, 0.1)
    print(np.min(a))
    print(np.max(a))
    return a

def test():
    a = cv2.imread('sample5.jpg')
    b = cv2.imread('sample6.jpg')
    c = find_keypoints(a)

    a[c>0.05*c.max()] = [0,0,255]

    c[c>0.05*c.max()] = 100
    c[c<100] = 0
    c[c>1] = 1
    print(np.sum(c))

    '''

    a = imutils.resize(a, width=500)
    b = imutils.resize(b, width=500)

    kpA, kpB = match_features_orb(a, b)

    for i in range(0, len(kpA)):
        point = kpA[i].pt
        point = (int(point[0]), int(point[1]))
        cv2.circle(a,point, 7, (0,0,255), -1)
    for i in range(0, len(kpB)):
        point = kpB[i].pt
        point = (int(point[0]), int(point[1]))
        cv2.circle(b,point, 7, (0,0,255), -1)
    '''
    cv2.imshow('A', a)
    cv2.imshow('B', b)
    cv2.waitKey(0)
    

    

#test()

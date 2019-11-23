import cv2
from matplotlib import pyplot as plt

orb = cv2.ORB_create()
FLANN_INDEX_LSH = 6

def match_features_orb(im1, im2):
    kpA, desA = orb.detectAndCompute(im1, None)
    kpB, desB = orb.detectAndCompute(im2, None)
    index_params = dict(algorithm = FLANN_INDEX_LSH, table_number = 6, key_size = 12, multi_probe_level = 1)
    flann = cv2.FlannBasedMatcher(index_params, dict())
    matches = flann.knnMatch(desA, desB, k=2)
    goodKeyPointsA = []
    goodKeyPointsB = []
    for i, match in enumerate(matches):
        if len(match) < 2:
            print(i, "could not unpack error")
            continue
        m, n = match
        if m.distance < 0.7 * n.distance: # Aparently determined in some paper to work well
            goodMatch = m
            goodKeyPointsA.append(kpA[goodMatch.queryIdx])
            goodKeyPointsB.append(kpB[goodMatch.trainIdx])

    return goodKeyPointsA, goodKeyPointsB

def match_features_orb_desc(kpA, desA, im2):
    kpB, desB = orb.detectAndCompute(im2, None)
    index_params = dict(algorithm = FLANN_INDEX_LSH, table_number = 6, key_size = 12, multi_probe_level = 1)
    flann = cv2.FlannBasedMatcher(index_params, dict())
    matches = flann.knnMatch(desA,desB,k=2)
    # print(matches[0])
    for i,(m,n) in enumerate(matches):
        print(matches[i])
        if m.distance >= 0.7 *n.distance: # Aparently determined in some paper to work well
            matches[i] = 'Apple'
    matches[:] = [match for match in matches if match != 'Apple']
    
    return kpA, kpB, desA, desB, matches

def test():
    a = cv2.imread('/Users/kyleaj/Pictures/1.jpg')
    b = cv2.imread('/Users/kyleaj/Pictures/2.jpg')
    kpA, kpB = match_features_orb(a, b)

    for i in range(0, len(kpA)):
        point = kpA[i].pt
        point = (int(point[0]), int(point[1]))
        cv2.circle(a,point, 7, (0,0,255), -1)
    for i in range(0, len(kpB)):
        point = kpB[i].pt
        point = (int(point[0]), int(point[1]))
        cv2.circle(b,point, 7, (0,0,255), -1)

    cv2.imshow('A', a)
    cv2.imshow('B', b)
    cv2.waitKey(0)

if __name__ == '__main__':
    test()

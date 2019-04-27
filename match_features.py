import cv2
from matplotlib import pyplot as plt

orb = cv2.ORB_create()
FLANN_INDEX_LSH = 6

def match_features_orb(im1, im2):
    kpA, desA = orb.detectAndCompute(im1, None)
    kpB, desB = orb.detectAndCompute(im2, None)
    index_params = dict(algorithm = FLANN_INDEX_LSH, table_number = 6, key_size = 12, multi_probe_level = 1)
    flann = cv2.FlannBasedMatcher(index_params, dict())
    matches = flann.knnMatch(desA,desB,k=2)
    print(len(matches))
    matchesMask = [[0,0] for i in range(len(matches))]
    for i,(a,b,c,d,e) in enumerate(zip(matches, kpA, kpB, desA, desB)):
        m,n = a
        print("TRIAL", i)
        print(matches[i])
        if m.distance < 0.7 *n.distance: # Aparently determined in some paper to work well
            matchesMask[i]=[1,0]
            
            # matches[i] = 'Apple'
            # kpA[i] = 'Apple'
            # kpB[i] = 'Apple'
            # desA[i] = 'Apple'
            # desB[i] = 'Apple'
            print(matches[i])
    matches[:] = [match for match in matches if match != 'Apple']
    kpA[:] = [kp for kp in kpA if kp != 'Apple']
    kpB[:] = [kp for kp in kpB if kp != 'Apple']
    # desA[:] = [des for des in desA if des != 'Apple']
    # desB[:] = [des for des in desB if des != 'Apple']
    print(len(matches))
    
    return kpA, kpB, desA, desB, matches, matchesMask

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
    kpA, kpB, desA, desB, matches, matchesMask = match_features_orb(a, b)
    print(len(kpA))
    draw_params = dict(matchColor = (0,255,0),
                   singlePointColor = (255,0,0),
                   matchesMask = matchesMask,
                   flags = 0)

    img3 = cv2.drawMatchesKnn(a,kpA,b,kpB,matches,None,**draw_params)
    plt.imshow(img3,),plt.show()

test()
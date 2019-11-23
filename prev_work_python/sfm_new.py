from match_features import match_features_orb as mf
import sys
import cv2
import numpy as np
import imutils

focal_length = 28 / 1000

W = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]
InvW = [[0, 1, 0], [-1, 0, 0], [0, 0, 1]]
Z = [[0, 1, 0], [-1, 0, 0], [0, 0, 0]]

def get_essential_matrix(kpA, kpB):
    assert(len(kpA) == len(kpB))
    # print(len(kpA))

    coefficient_matrix = np.zeros((len(kpA), 9))
    for i in range(len(kpA)):
        pointA = kpA[i].pt
        pointB = kpB[i].pt
        coefficient_matrix[i][0] = pointA[0] * pointB[0]
        coefficient_matrix[i][1] = pointA[1] * pointB[0] 
        coefficient_matrix[i][2] = pointB[0]
        coefficient_matrix[i][3] = pointA[0] * pointB[1]
        coefficient_matrix[i][4] = pointA[1] * pointB[1]
        coefficient_matrix[i][5] = pointB[1]
        coefficient_matrix[i][6] = pointA[0]
        coefficient_matrix[i][7] = pointA[1]
        coefficient_matrix[i][8] = 1

    U, D, V_t = np.linalg.svd(coefficient_matrix, full_matrices = False)
    essential = np.reshape(V_t[-1], (3, 3))

    U2, D2, Vt2 = np.linalg.svd(essential)
    # set D to [1 1 0]?
    D2 = [1, 1, 0]

    print("Diagonal Matrix:")
    print(D2)

    essential = np.matmul(np.matmul(U2, np.diag(D2)), Vt2)
    t = U2 @ W @ np.diag(D2) @ U2.T
    R = U2 @ InvW @ Vt2
    return essential, t, R

def get_epipole(essential, pointA, pointB):
    x = np.append(np.array(pointB), 1)
    xt = np.transpose(np.append(np.array(pointA), 1))
    
    # print(x)
    # print(xt)
    
    result = np.matmul(xt, np.matmul(essential, x))

    return result

def main():

    image1 = sys.argv[1]
    image2 = sys.argv[2]

    a = cv2.imread(image1)
    b = cv2.imread(image2)

    print(image1, image2)
    print(a, b)

    a = imutils.resize(a, width=500)
    b = imutils.resize(b, width=500)

    kpA, kpB = mf(a, b)
    

    for i in range(0, len(kpA)):
        point = kpA[i].pt
        point = (int(point[0]), int(point[1]))
        cv2.circle(a,point, 7, (0,0,255), -1)
    for i in range(0, len(kpB)):
        point = kpB[i].pt
        point = (int(point[0]), int(point[1]))
        cv2.circle(b,point, 7, (0,0,255), -1)

    #cv2.imshow('A', a)
    #cv2.imshow('B', b)
    #cv2.waitKey(0)

    #keyPointsA = [[1,2],[3,4]]
    #keyPointsB = [[5,6],[7,8]]

    e, t, r = get_essential_matrix(kpA, kpB)
    print("ESSENTIAL MATRIX")
    print(e)
    print("ROTATION")
    print(r)

    t1 = t[2][1]
    t2 = t[0][2]
    t3 = t[1][0]
    t_v = [t1, t2, t3]

    print("TRANSLATION")
    print(t_v)

    for i in range(len(kpA)):
        error = get_epipole(e, kpA[i].pt, kpB[i].pt)
        # print("ERROR: ", error)

if __name__ == '__main__':
    main()

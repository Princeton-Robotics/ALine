import match_features
import numpy as np
import cv2
import sys
np.set_printoptions(threshold=sys.maxsize)


def estimateF(pointsA, pointsB):
    assert(len(pointsA) == len(pointsB))
    A = np.zeros((len(pointsA), 9))
    for i in range(len(pointsA)):
        x = pointsA[i, 0]
        y = pointsA[i, 1]

        xp = pointsB[i, 0]
        yp = pointsB[i, 1]

        row = [x * xp, y * xp, xp, x*yp, y*yp, yp, x, y, 1]
        A[i, :] = row
    print(A)

    u, s, v = np.linalg.svd(A)
    print(v.shape)
    f = np.reshape(v[:,-1], (3,3))
    fu, fs, fv = np.linalg.svd(f)
    fv[2,2] = 0
    #print(f)
    f = np.matmul(fu, np.matmul(np.diag(fs), fv))
    print(f)
    return f


def main():
    pointsA, pointsB = match_features.test()
    pointsA = np.array(pointsA)
    pointsB = np.array(pointsB)
    # print(pointsA.shape)
    F, mask = cv2.findFundamentalMat(pointsB, pointsA, cv2.FM_RANSAC)
    # F = estimateF(pointsA, pointsB)
    pointsA = pointsA[mask.ravel()==1]
    pointsB = pointsB[mask.ravel()==1]

    print(pointsA)

    sum = 0

    for i in range(len(pointsA)):
        point1 = [pointsA[i,0],pointsA[i,1], 1]
        point2 = [pointsB[i,0],pointsB[i,1], 1]
        sum = sum + abs(np.matmul(point1, np.matmul(F, point2)))

    sum = sum / len(pointsA)
    print('Mean algebraic error: ' + str(sum))

    



if __name__ == '__main__':
    main()


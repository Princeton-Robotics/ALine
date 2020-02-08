from match_features import match_features_orb as mf
import sys
import cv2
import numpy as np
import imutils
import matplotlib
from mpl_toolkits.mplot3d import Axes3D

FOCAL_LENGTH = 26

Z = [[0, 1, 0], [-1, 0, 0], [0, 0, 0]]
K = np.diag([FOCAL_LENGTH, FOCAL_LENGTH, 1])

def find_eigenvalues(A):
    U, D, V_t = np.linalg.svd(A)
    print("Eigenvalues:")
    print(D)

def analyze_keypoints(pointsA, pointsB):

    essential_matrix, _ = cv2.findEssentialMat(pointsA, pointsB, K)

    return essential_matrix
    
 #   U, D, V_t = np.linalg.svd(essential_matrix, full_matrices = False)
 #   print(D)
 #   D[0] = 1
 #   D[1] = 1
 #   D[2] = 0

 #   essential_matrix = U @ np.diag(D) @ V_t

 #   return essential_matrix

def triangulate(essential_matrix, points1, points2):
    retval, R, t, mask, homogenousPoints = cv2.recoverPose(essential_matrix, points1, points2, K, 10000, None, None, None, None)
    triangulatedPoints = homogenousPoints[0:3, :] / homogenousPoints[3, :]
    return triangulatedPoints

def main():
    image1 = sys.argv[1]
    image2 = sys.argv[2]

    img1 = cv2.imread(image1)
    img2 = cv2.imread(image2)

    img1 = imutils.resize(img1, width=500)
    img2 = imutils.resize(img2, width=500)

    keypoints1, keypoints2 = mf(img1, img2)
    assert(len(keypoints1) == len(keypoints2))

    pointsA = []
    pointsB = []
    for i in range(len(keypoints1)):
        pointsA.append(keypoints1[i].pt)
        pointsB.append(keypoints2[i].pt)

    pointsA = np.array(pointsA)
    pointsB = np.array(pointsB)

    print("POINTSA")
    print(pointsA.shape)
    print("POINTSB")
    print(pointsB.shape)

    for i in range(0, len(keypoints1)):
        point = keypoints1[i].pt
        point = (int(point[0]), int(point[1]))
        cv2.circle(img1, point, 7, (0, 0, 20*i % 255), -1)
    for i in range(0, len(keypoints2)):
        point = keypoints2[i].pt
        point = (int(point[0]), int(point[1]))
        cv2.circle(img2, point, 7, (0, 0, 20*i % 255), -1)

    # validate_key_points(img1, img2)

    essential_matrix = analyze_keypoints(pointsA, pointsB)
    print("ESSENTIAL MATRIX")
    print(essential_matrix)

    print("TRIANGULATED POINTS")
    print(triangulate(essential_matrix, pointsA, pointsB))

    cv2.imshow("A", img1)
    cv2.imshow("B", img2)

    cv2.waitKey(0)

if __name__ == '__main__':
    main()

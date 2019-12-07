from match_features import match_features_orb as mf
from triangles import triangulation
import sys
import cv2
import numpy as np
import imutils
import matplotlib
from mpl_toolkits.mplot3d import Axes3D

FOCAL_LENGTH = 26

W = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]
InvW = [[0, 1, 0], [-1, 0, 0], [0, 0, 1]]
Z = [[0, 1, 0], [-1, 0, 0], [0, 0, 0]]
K = np.diag([FOCAL_LENGTH, FOCAL_LENGTH, 1])

def find_eigenvalues(A):
    U, D, V_t = np.linalg.svd(A)
    print("Eigenvalues:")
    print(D)

def analyze_keypoints(keypoints1, keypoints2):
    assert(len(keypoints1) == len(keypoints2))

    pointsA = []
    pointsB = []
    for i in range(len(keypoints1)):
        pointsA.append(keypoints1[i].pt)
        pointsB.append(keypoints2[i].pt)

    pointsA = np.array(pointsA)
    pointsB = np.array(pointsB)

    print(pointsA.shape)
    print(pointsB.shape)
    print(K.shape)

    essential_matrix, _ = cv2.findEssentialMat(pointsA, pointsB, K)

    U, D, V_t = np.linalg.svd(essential_matrix, full_matrices = False)
    print(D)
    D[0] = 1
    D[1] = 1
    D[2] = 0

    essential_matrix = U @ np.diag(D) @ V_t

    translation = U @ W @ np.diag(D) @ U.T
    rotation1 = U @ np.matrix(InvW) @ V_t
    rotation2 = U @ np.matrix(InvW).T @ V_t

    return essential_matrix, translation, [rotation1, rotation2]

def get_epipole(essential, pointA, pointB):
    x = np.append(np.array(pointB), 1)
    xt = np.transpose(np.append(np.array(pointA), 1))
    
    result = xt @ essential @ x

    return result

def find_epipole_error(keypoints, essential_matrix):
    total_error = 0
    for point in keypoints:
        total_error += get_epipole(essential_matrix, point.pt, point.pt)
    print("Average Error:")
    print(total_error / len(keypoints))

def validate_key_points(img1, img2):
    cv2.imshow('Image 1', img1)
    cv2.imshow('Image 2', img2)
    cv2.waitKey(0)

def print_3d_points(point_array):
    print("POINTS")
    for pt in point_array:
        print(pt)

def main():
    image1 = sys.argv[1]
    image2 = sys.argv[2]

    img1 = cv2.imread(image1)
    img2 = cv2.imread(image2)

    img1 = imutils.resize(img1, width=500)
    img2 = imutils.resize(img2, width=500)

    keypoints1, keypoints2 = mf(img1, img2)

    for i in range(0, len(keypoints1)):
        point = keypoints1[i].pt
        point = (int(point[0]), int(point[1]))
        cv2.circle(img1, point, 7, (0, 0, 20*i % 255), -1)
    for i in range(0, len(keypoints2)):
        point = keypoints2[i].pt
        point = (int(point[0]), int(point[1]))
        cv2.circle(img2, point, 7, (0, 0, 20*i % 255), -1)

    # validate_key_points(img1, img2)

    essential_matrix, translation_matrix, rotations = analyze_keypoints(keypoints1, keypoints2)
    print("ESSENTIAL MATRIX")
    print(essential_matrix)
    print("ROTATIONS")
    print(rotations)

    t1 = translation_matrix[2][1]
    t2 = translation_matrix[0][2]
    t3 = translation_matrix[1][0]
    translation = np.array([t1, t2, t3])
    
    translations = [translation, -1 * translation]

    print("TRANSLATION")
    print(translation)

    print(essential_matrix @ translation)

    find_epipole_error(keypoints1, essential_matrix)

    min = np.inf
    best_reconstruct = []
    point_pairs = zip(keypoints1, keypoints2)
    for rotation in rotations:
        for translation in translations:
            counter = 0
            for point_pair in point_pairs:
                val = triangulation(rotation, translation, K, point_pair[0].pt, point_pair[1].pt)
                if val is None:
                    counter = counter + 1
            if counter < min:
                min = counter
                best_reconstruct = (rotation, translation)

    print("MIN")
    print(min)

    points_in_3D_x = []
    points_in_3D_y = []
    points_in_3D_z = []
    for point_pair in point_pairs:
        val = triangulation(best_reconstruct[0], best_reconstruct[1], K, point_pair[0].pt, point_pair[1].pt)
        if not val is None:
            points_in_3D_x.append(val[0])
            points_in_3D_y.append(val[1])
            points_in_3D_z.append(val[2])

    Axes3D.scatter(points_in_3D_x, points_in_3D_y, points_in_3D_z)

    # print_3d_points(points_in_3d)

if __name__ == '__main__':
    main()

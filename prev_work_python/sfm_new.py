from match_features import match_features_orb as mf
import sys
import cv2
import numpy as np
import imutils

focal_length = 28 / 1000

W = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]
InvW = [[0, 1, 0], [-1, 0, 0], [0, 0, 1]]
Z = [[0, 1, 0], [-1, 0, 0], [0, 0, 0]]

def find_eigenvalues(A):
    U, D, V_t = np.linalg.svd(A, full_matrices=False)
    print("Eigenvalues:")
    print(D)

def analyze_keypoints(keypoints1, keypoints2):
    assert(len(keypoints1) == len(keypoints2))

    coefficient_matrix = np.zeros((len(keypoints1), 9))
    for i in range(len(keypoints1)):
        pointA = keypoints1[i].pt
        pointB = keypoints2[i].pt
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
    essential_matrix = np.reshape(V_t[-1], (3, 3))

    U2, D2, Vt2 = np.linalg.svd(essential_matrix)
    D2 = [1, 1, 0]

    essential_matrix = U2 @ np.diag(D2) @ Vt2
    translation = U2 @ W @ np.diag(D2) @ U2.T
    rotation = U2 @ InvW @ Vt2

    # find_eigenvalues(rotation)

    return essential_matrix, translation, rotation

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
        cv2.circle(img1, point, 7, (0,0,255), -1)
    for i in range(0, len(keypoints2)):
        point = keypoints2[i].pt
        point = (int(point[0]), int(point[1]))
        cv2.circle(img2, point, 7, (0,0,255), -1)

    # validate_key_points(img1, img2)

    essential_matrix, translation_matrix, rotation = analyze_keypoints(keypoints1, keypoints2)
    print("ESSENTIAL MATRIX")
    print(essential_matrix)
    print("ROTATION")
    print(rotation)

    t1 = translation_matrix[2][1]
    t2 = translation_matrix[0][2]
    t3 = translation_matrix[1][0]
    translation = [t1, t2, t3]

    print("TRANSLATION")
    print(translation)

    find_epipole_error(keypoints1, essential_matrix)

if __name__ == '__main__':
    main()

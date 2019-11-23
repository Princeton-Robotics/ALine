import numpy as np

def triangulation(r, t, k, p1, p2):
    invK = np.linalg.inv(k)
    h1 = np.array([p1[0], p1[1], 1])
    h2 = np.array([p2[0], p2[1], 1])

    a = hat(invK @ h2)
    b = invK @ h1

    part1 = a @ b
    part2 = a @ t

    z1 = -part1 / part2

    return invK @ z1 @ h1

def hat(v):
    return np.array([[0, -v[2], v[1]],
                     [v[2], 0, -v[0]],
                     [-v[1], v[0], 0])
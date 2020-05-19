import numpy as np


def G(r, m):
    if r == 0:
        return np.ones((1, 2**m))  # 2^m 1's
    elif r == m:
        return np.identity(2**m)  # unit matrix of size 2^m
    else:
        M = G(r, m-1)
        N = G(r-1, m-1)
        z = np.zeros(N.shape)
        upper = np.concatenate((M, M), axis=1)
        lower = np.concatenate((z, N), axis=1)
        return np.concatenate((upper, lower), axis=0)


def bin_array(num, m):
    """Convert a positive integer num into an m-bit bit vector"""
    return np.array(list(np.binary_repr(num).zfill(m))).astype(np.int8)


def error_vec(idx, m):
    err = np.zeros((1, m))
    err[0][idx] = 1
    return err


def binify_vector(vec):
    newVec = np.zeros(vec.shape)
    for (idx, val) in enumerate(vec):
        newVec[idx] = (val % 2)
    return newVec


def binify_matrix(mat):
    newMat = np.zeros(mat.shape)
    for (idx, vec) in enumerate(mat):
        newMat[idx] = binify_vector(vec)
    return newMat


G = G(1, 3)
G_t = G.transpose()
for vec in [binify_vector(bin_array(i, 4).dot(G)) for i in range(16)]:
    # print(vec)
    continue


verify = binify_matrix(G.dot(G_t))
# print(verify)


for vec in [error_vec(i, 8) for i in range(8)]:
    # print(vec.dot(G_t))
    continue


print(binify_vector(np.array([0, 1, 1, 1, 0, 0, 1, 1]).dot(G_t)))

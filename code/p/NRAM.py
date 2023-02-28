import numpy as np
import matplotlib.pyplot as plt
import cv2
import math
import scipy


def init(path):
    pic = plt.imread(path)
    plt.figure()
    plt.subplot(131)
    plt.title('Original')
    if pic.ndim == 2:
        plt.imshow(pic, cmap='gray')
    if pic.ndim == 3:
        plt.imshow(pic)
        pic = cv2.cvtColor(pic, cv2.COLOR_RGB2GRAY)
    pic = np.float64(pic)

    return pic


def gen_patch(pic, patch_size=40, slide_step=40):

    pic_H, pic_W = np.shape(pic)[0:2]

    row_patch_num = math.ceil((pic_H - patch_size) / slide_step + 1)
    col_patch_num = math.ceil((pic_W - patch_size) / slide_step + 1)
    row_pos_arr = list(range(0, slide_step * (row_patch_num - 1), slide_step))
    row_pos_arr.append(pic_H - patch_size)
    col_pos_arr = list(range(0, slide_step * (col_patch_num - 1), slide_step))
    col_pos_arr.append(pic_W - patch_size)

    Patch = np.zeros((patch_size, patch_size, row_patch_num * col_patch_num))
    k = 0
    for j in col_pos_arr:
        for i in row_pos_arr:
            patch_cell = pic[i:i + patch_size, j:j + patch_size]
            Patch[:, :, k] = patch_cell
            k += 1

    return Patch


def res_patch(patch, pic, patch_size=40, slide_step=40):

    pic_H, pic_W = np.shape(pic)[0:2]

    row_patch_num = math.ceil((pic_H - patch_size) / slide_step + 1)
    col_patch_num = math.ceil((pic_W - patch_size) / slide_step + 1)
    row_pos_arr = list(range(0, slide_step * (row_patch_num - 1), slide_step))
    row_pos_arr.append(pic_H - patch_size)
    col_pos_arr = list(range(0, slide_step * (col_patch_num - 1), slide_step))
    col_pos_arr.append(pic_W - patch_size)

    accImg = np.zeros((pic_H, pic_W))
    weiImg = np.zeros((pic_H, pic_W))
    onesMat = np.ones((patch_size, patch_size))
    k = 0
    for j in col_pos_arr:
        for i in row_pos_arr:
            tempPatch = np.reshape(patch[:, :, k], (patch_size, patch_size))
            accImg[i:i+patch_size, j:j+patch_size] = tempPatch
            weiImg[i:i+patch_size, j:j+patch_size] = onesMat
            k += 1

    return accImg / weiImg


def structure_tensor_lambda(pic, size=3):
    Gaussian_kernel = cv2.getGaussianKernel(size, 2) @ cv2.getGaussianKernel(3, 2).T
    u = scipy.ndimage.convolve(pic, Gaussian_kernel)
    Gx, Gy = np.gradient(u)

    Gaussian_kernel = cv2.getGaussianKernel(size, 9) @ cv2.getGaussianKernel(3, 9).T
    J_11 = scipy.ndimage.convolve(Gx * Gx, Gaussian_kernel)
    J_12 = scipy.ndimage.convolve(Gx * Gy, Gaussian_kernel)
    J_21 = J_12
    J_22 = scipy.ndimage.convolve(Gy * Gy, Gaussian_kernel)

    sqrt_delta = ((J_11 - J_22) ** 2 + 4 * (J_12 ** 2)) ** (1 / 2)
    lambda1 = 0.5 * (J_11 + J_22 + sqrt_delta)
    lambda2 = 0.5 * (J_11 + J_22 - sqrt_delta)

    return lambda1, lambda2


def prox_pstnn(Y, N, mu):
    dim = Y.shape
    X = np.zeros(dim, dtype='complex')
    Y = np.fft.fft(Y)
    tau = 1 / mu

    U, diagS, V = np.linalg.svd(Y[:, :, 0])
    des_S = np.sort(diagS)[::-1]
    idx_S = np.argsort(diagS)[::-1]
    des_U, des_V = U[:, idx_S], V.T[:, idx_S]
    U1, diagS1, V1 = des_U[:, 0:N+1], des_S[0:N+1], des_V[:, 0:N+1]
    U2, diagS2, V2 = des_U[:, N+1:], des_S[N+1:], des_V[:, N+1:]
    threshS2 = np.fmax(diagS2 - tau, 0)
    X[:, :, 0] = U1 @ np.diag(diagS1) @ V1.T + U2 @ np.diag(threshS2) @ V2.T

    half_n3 = round(dim[2] / 2)
    for i in range(1, half_n3 + 1):
        U, diagS, V = np.linalg.svd(Y[:, :, i])
        des_S = np.sort(diagS)[::-1]
        idx_S = np.argsort(diagS)[::-1]
        des_U, des_V = U[:, idx_S], V.T[:, idx_S]
        U1, diagS1, V1 = des_U[:, 0:N+1], des_S[0:N+1], des_V[:, 0:N+1]
        U2, diagS2, V2 = des_U[:, N+1:], des_S[N+1:], des_V[:, N+1:]
        threshS2 = np.fmax(diagS2 - tau, 0)
        X[:, :, i] = U1 @ np.diag(diagS1) @ V1.T + U2 @ np.diag(threshS2) @ V2.T
        X[:, :, dim[2] - i] = np.conj(X[:, :, i])

    if dim[2] % 2 == 0:
        i = half_n3 + 1
        U, diagS, V = np.linalg.svd(Y[:, :, i])
        des_S = np.sort(diagS)[::-1]
        idx_S = np.argsort(diagS)[::-1]
        des_U, des_V = U[:, idx_S], V.T[:, idx_S]
        U1, diagS1, V1 = des_U[:, 0:N+1], des_S[0:N+1], des_V[:, 0:N + 1]
        U2, diagS2, V2 = des_U[:, N+1:], des_S[N+1:], des_V[:, N+1:]
        threshS2 = np.fmax(diagS2 - tau, 0)
        X[:, :, i] = U1 @ np.diag(diagS1) @ V1.T + U2 @ np.diag(threshS2) @ V2.T

    X = np.fft.ifft(X)

    return X.real


def prox_l1(b, lambda_):
    x = np.fmax(0, b - lambda_) + np.fmin(0, b + lambda_)
    x = np.fmax(x, 0)

    return x


def rankN(x, ration_n):

    num3 = np.shape(x)[2]
    re_x = x.reshape(num3, -1, order='F')
    S_diag = np.linalg.svd(re_x)[1]
    des_S = np.sort(S_diag)[::-1]
    ratioVec = des_S / des_S[0]
    idxArr = np.where(ratioVec < ration_n)[0]
    if idxArr[0] > 0:
        N = idxArr[0] - 1
    else:
        N = 0

    return N


def trpca_pstnn(X, lambda_, tenW, tol=1e-3, max_iter=500, rho=1.05, mu=2e-3, max_mu=1e10, debug=None):

    N = rankN(X, 0.1)

    dim = np.shape(X)
    L = np.zeros(dim)
    S = np.zeros(dim)
    Y = np.zeros(dim)
    weightTen = np.ones(dim)

    for iter in range(max_iter):
        preT = np.sum(S > 0)

        R = -S + X - Y / mu
        L = prox_pstnn(R, N, mu)

        T = -L + X - Y / mu
        S = prox_l1(T, weightTen * lambda_ / mu)
        weightTen = N+1 / (np.abs(S) + 0.01) / tenW

        dY = L + S - X
        err = np.linalg.norm(dY) / np.linalg.norm(X)
        currT = np.sum(S[:] > 0)

        if debug:
            print("iter: %d , mu: %.4f, err: %.4f, |T|0: %d" % (iter, mu, err, int(currT)))

        if err < tol or (0 < preT == currT > 0):
            break

        Y = Y + dY * mu
        mu = min(rho * mu, max_mu)

    return L, S


lambdaL = 0.7

img = init("./1.bmp")
D = gen_patch(img)

n1, n2, n3 = D.shape

lambDa1, lambDa2 = structure_tensor_lambda(img)
cornerStrength = (lambDa1 * lambDa2) / (lambDa1 + lambDa2)
maxValue = np.maximum(lambDa1, lambDa2)
priorWeight = np.zeros(maxValue.shape, np.float64)
cv2.normalize(cornerStrength * maxValue, priorWeight, 1.0, 0.0, cv2.NORM_MINMAX, dtype=cv2.CV_64F)
W = gen_patch(priorWeight)

lambda0 = lambdaL / math.sqrt(max(n1, n2) * n3)

B, T_ = trpca_pstnn(D, lambda0, W)

tarImg = res_patch(T_, img)
backImg = res_patch(B, img)

maxV = np.max(img)
E = cv2.normalize(tarImg, None, 1, 0, cv2.NORM_MINMAX, dtype=cv2.CV_64F)*maxV
E = E.astype(np.uint8)
A = cv2.normalize(backImg, None, 1, 0, cv2.NORM_MINMAX, dtype=cv2.CV_64F)*maxV
A = A.astype(np.uint8)
plt.subplot(132)
plt.imshow(E, cmap='gray')
plt.title("Target")
plt.subplot(133)
plt.imshow(A, cmap='gray')
plt.title("Background")

plt.show()

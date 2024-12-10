import logging
import math
import os
import time

import cv2
import numpy as np


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("process.log"),
        logging.StreamHandler()
    ]
)

logging.info("Program started")

logging.info(f"Current working directory: {os.getcwd()}")

path_to_img = os.path.join('K:\\', 'Pyth', 'TMP', 'prog-instruments-labs', 'lab_4', '1.jpg')
img = cv2.imread(path_to_img, cv2.IMREAD_GRAYSCALE)
if img is None:
    logging.error("Error loading image. File '1.jpg' not found.")
    exit()

logging.info(f"Image loaded: height={img.shape[0]}, width={img.shape[1]}")

step = 3
shift_x_y = np.array([1, 2, 3, 4, 5])
rot = np.array([-5, -4, -3, -2, -1])
list_img_min = []
list_img_obr = []
h, w = img.shape[:2]
center = (int(w / 2), int(h / 2))


def scale(img, item_r, item_tr):
    logging.debug(f"Starting scale processing with parameters item_r={item_r}, item_tr={item_tr}")
    translation_matrix = np.float32([[1, 0, item_tr], [0, 1, item_tr]])
    rotation_matrix = cv2.getRotationMatrix2D(center, item_r, 1)
    img_tr = cv2.warpAffine(img, translation_matrix, (w, h))
    img_tr_rot = cv2.warpAffine(img_tr, rotation_matrix, (w, h))

    img_rot_blur3 = cv2.GaussianBlur(img_tr_rot, (step, step), 0)

    img_min = np.zeros((math.ceil(h / step), math.ceil(w / step)), np.uint8)
    k = m = 0
    for i in range(1, h, step):
        for j in range(1, w, step):
            img_min[k, m] = img_rot_blur3[i, j]
            m += 1
        m = 0
        k += 1
    logging.debug("Scale processing completed")
    return img_min


def upscale(img_min, item_r, item_tr):
    logging.debug(f"Starting upscale processing with parameters item_r={item_r}, item_tr={item_tr}")
    img_obr = np.zeros((h, w), np.uint8)
    k = m = 0
    for i in range(1, h, step):
        for j in range(1, w, step):
            img_obr[i, j] = img_min[k, m]
            m += 1
        m = 0
        k += 1

    img_obr_blur3 = cv2.GaussianBlur(img_obr, (step, step), 0)

    rotation_matrix_obr = cv2.getRotationMatrix2D(center, item_r * (-1), 1)
    translation_matrix_obr = np.float32([[1, 0, item_tr * (-1)], [0, 1, item_tr * (-1)]])
    img_obr_blur3_rot = cv2.warpAffine(img_obr_blur3, rotation_matrix_obr, (w, h))
    img_obr = cv2.warpAffine(img_obr_blur3_rot, translation_matrix_obr, (w, h))
    logging.debug("Upscale processing completed")
    return img_obr


start = time.time()
logging.info("Starting main image processing loop")
for item_r, item_tr in zip(rot, shift_x_y):
    list_img_min.append(scale(img, item_r, item_tr))
    list_img_obr.append(upscale(scale(img, item_r, item_tr), item_r, item_tr))
end = time.time()
logging.info(f"Main loop completed. Execution time: {end - start:.2f} seconds")

logging.info("Starting image restoration")
alfa = 0.2
img_HR_cur = np.zeros((h, w), np.uint8)
diff_img_min = np.zeros((math.ceil(h / step), math.ceil(w / step)), np.uint8)

for inter in range(1, 15, 1):
    for img_min_LR, item_r, item_tr in zip(list_img_min, rot, shift_x_y):
        try:
            img_min_cur = scale(img_HR_cur, item_r, item_tr)
            diff_img_min = img_min_LR - img_min_cur
            diff_HR = upscale(diff_img_min, item_r, item_tr)

            for i in range(0, h, 1):
                for j in range(0, w, 1):
                    img_HR_cur[i, j] = img_HR_cur[i, j] + alfa * diff_HR[i, j]
        except Exception as e:
            logging.error(f"Restoration error for item_r={item_r}, item_tr={item_tr}: {e}")

logging.info("Image restoration completed")

cv2.imshow('img', img)
cv2.waitKey(0)
cv2.imshow('res', img_HR_cur)
cv2.waitKey(0)

logging.info("Starting metrics calculation")


def mse(img, img_sh):
    return np.mean((img - img_sh) ** 2)


def psnr(img, img_sh):
    return 10 * math.log10(255.0 ** 2 / mse(img, img_sh))


def ssim(img1, img2):
    C1 = (0.01 * 255) ** 2
    C2 = (0.03 * 255) ** 2
    kernel = cv2.getGaussianKernel(3, 0)
    window = np.outer(kernel, kernel.transpose())

    mu1 = cv2.filter2D(img1, -1, window)[1:-1, 1:-1]
    mu2 = cv2.filter2D(img2, -1, window)[1:-1, 1:-1]

    sigma1_sq = cv2.filter2D(img1 ** 2, -1, window)[1:-1, 1:-1] - mu1 ** 2
    sigma2_sq = cv2.filter2D(img2 ** 2, -1, window)[1:-1, 1:-1] - mu2 ** 2
    sigma12 = cv2.filter2D(img1 * img2, -1, window)[1:-1, 1:-1] - mu1 * mu2

    ssim_map = ((2 * mu1 * mu2 + C1) * (2 * sigma12 + C2)) / ((mu1 ** 2 + mu2 ** 2 + C1) *
                                                              (sigma1_sq + sigma2_sq + C2))
    return ssim_map.mean()


img = img.astype(np.float64)
img_HR_cur = img_HR_cur.astype(np.float64)
logging.info(f"MSE: {mse(img, img_HR_cur)}")
logging.info(f"PSNR: {psnr(img, img_HR_cur)}")
logging.info(f"SSIM: {ssim(img, img_HR_cur)}")

logging.info("Program finished")
import numpy as np
import cv2 as cv
import os


def get_four_point(point):
    temp_x, temp_y = point

    x1 = int(temp_x)
    y1 = int(temp_y)

    x2 = x1
    y2 = y1 + 1

    x3 = x1 + 1
    y3 = y1

    x4 = x1 + 1
    y4 = y1 + 1

    u = temp_x - x1
    v = temp_y - y1

    return [x1, y1], [x2, y2], [x3, y3], [x4, y4], [u, v]


def calculate_delta_x(point1, point2):
    hypotenuse = calculate_line_point(point1, point2)
    delta_x = abs(point1[0] - point2[0]) / np.round(hypotenuse)
    return delta_x


def read_tiff(file_path):
    img = cv.imread(file_path, 2)
    if np.sum(img) == 0:
        print("[ Read Tiff Error ] {} not found ! ".format(file_path))
        exit(0)
    return img


def rename_column(crf_index, file_index_):
    # return "crf_{}_{}".format(crf_index, os.path.basename(file_index_))
    return "crf_{}".format(crf_index)


def watch_data(data):
    for step, _ in enumerate(data):
        print("{} {}".format(step, data[step]))


def calculate_line_point(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    hypotenuse = np.sqrt(np.square(x1 - x2) + np.square(y1 - y2))
    return hypotenuse


def psnr_calculate(mse):
    rmse = np.sqrt(mse)
    psnr = 10 * np.log10(255 * 255 / mse)
    print(" mse = {} rmse = {} psnr = {}".format(mse, rmse, psnr))


if __name__ == '__main__':
    mse=333.19
    psnr_calculate(mse)

from utils.utils_common import read_tiff


def acquire_line_data(file_path, line_x, line_y):
    img = read_tiff(file_path)
    line_data = list()
    for step, x_index in enumerate(line_x):
        line_data.append(img[line_x[step], line_y[step]])
    return line_data


def acquire_double_linear_data(file_path, line_x, line_y):
    data = read_tiff(file_path)
    line_data = list()
    for step, _ in enumerate(line_x):
        x1, x2, x3, x4, u = line_x[step]
        y1, y2, y3, y4, v = line_y[step]
        # 插值
        im_value = (1 - u) * (1 - v) * int(data[x1, y1]) + (1 - u) * v * int(data[x2, y2]) + u * (
                1 - v) * int(data[x3, y3]) + u * v * int(data[x4, y4])
        line_data.append(im_value)
    return line_data


if __name__ == '__main__':
    pass

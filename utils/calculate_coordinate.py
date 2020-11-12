from utils.utils_common import calculate_delta_x, get_four_point
import matplotlib.pyplot as plt


def calculate_floor_coordinate(point1, point2):
    """
    计算point1到point2的坐标值 只求最长边 长度不是1
    :param point1:
    :param point2:
    :return: 直线经过的坐标值
    """
    x1, y1 = point1
    x2, y2 = point2
    assert abs(x1 - x2) + abs(y1 - y2) != 0
    x_list = list()
    y_list = list()
    change_x_y = False
    if abs(x1 - x2) < abs(y1 - y2):
        x1, y1, x2, y2 = y1, x1, y2, x2
        change_x_y = True
    if x1 > x2:
        x1, y1, x2, y2 = x2, y2, x1, y1
    gradient = (y2 - y1) / (x2 - x1)
    b = (y2 * x1 - y1 * x2) / (x1 - x2)
    for x_index in range(x1, x2 + 1):
        x_list.append(x_index)
        y_list.append(round(x_index * gradient + b))
    if change_x_y == True:
        x_list, y_list = y_list, x_list
    return x_list, y_list


def calculate_coordinate_double_linear(point1, point2):
    """
    计算point1到point2的坐标值 边长为1
    :param point1:
    :param point2:
    :return: 直线经过的坐标值
    """
    x1, y1 = point1
    x2, y2 = point2
    assert abs(x1 - x2) + abs(y1 - y2) != 0
    x_list = list()
    y_list = list()

    if x1 > x2:
        x1, y1, x2, y2 = x2, y2, x1, y1
    #  coordinate
    gradient = (y2 - y1) / (x2 - x1)
    b = (y2 * x1 - y1 * x2) / (x1 - x2)

    delta_x = calculate_delta_x([x1, y1], [x2, y2])

    x_index_ = x1
    while x_index_ - x2 < 1e-5:
        p1, p2, p3, p4, uv = get_four_point([x_index_, x_index_ * gradient + b])
        x_list.append([p1[0], p2[0], p3[0], p4[0], uv[0]])
        y_list.append([p1[1], p2[1], p3[1], p4[1], uv[1]])
        x_index_ += delta_x

    return x_list, y_list


def show_coordinate(p1, p2):
    x1, y1 = calculate_coordinate_double_linear(p1, p2)
    x2, y2 = calculate_coordinate_double_linear(p2, p1)
    assert x1 == x2 and y1 == y2
    plt.plot(x1, y1, 'r-o')
    plt.plot([p1[0], p2[0]], [p1[1], p2[1]])
    plt.grid()
    plt.show()


if __name__ == '__main__':
    pass

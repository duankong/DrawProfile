from utils.define_file_path import gather_file_name, gather_file_name_position
from utils.calculate_coordinate import calculate_coordinate_double_linear, calculate_floor_coordinate
from utils.acquire_im_data import acquire_line_data, acquire_double_linear_data
from utils.utils_common import rename_column, watch_data, calculate_line_point
from collections import namedtuple
import pandas as pd
import os
import numpy as np

Corrcoef_result_h264 = list()
Corrcoef_result_hevc = list()
Mse_result_h264 = list()
Mse_result_hevc = list()


def draw_profile(config, crf_index, result_path):
    file_index = int(config.index)
    point1, point2, position = config.point1, config.point2, config.position
    excel_filename = result_path + "data_{}_crf_{}_{}_position_[{}_{}]_point_[{},{}]_[{},{}].xlsx".format(
        file_index, crf_index[0], crf_index[-1], position[0], position[1],
        point1[0], point1[1], point2[0], point2[1])

    x, y = calculate_coordinate_double_linear(point1, point2)
    souce_data = []

    file_source_result, file_h264_result, file_hevc_result = gather_file_name_position(file_index, crf_index,
                                                                                       position)
    for _, file_index_ in enumerate(file_source_result):
        data = acquire_double_linear_data(file_index_, x, y)
        if os.path.basename(file_index_) == "a_convert_8bit_source_max_projection_{}_{}.tif".format(position[0],
                                                                                                    position[1]):
            souce_data = np.array(data)

    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    df3 = pd.DataFrame()

    corrcoef_array = list()
    mse_array = list()

    for step, file_index_ in enumerate(file_h264_result):
        data = np.array(acquire_double_linear_data(file_index_, x, y))
        corrcoef_ = np.corrcoef(souce_data, data)[0][1]
        mse_ = np.sum(np.square(data - souce_data)) / len(data)
        data = np.append(data, -1)
        data = np.append(data, corrcoef_)
        data = np.append(data, mse_)
        corrcoef_array.append(corrcoef_)
        mse_array.append(mse_)
        df2.insert(loc=0, value=np.array(data), column=rename_column(crf_index[step], file_index_))

    Corrcoef_result_h264.append([config, np.array(corrcoef_array).copy()])
    Mse_result_h264.append([config, np.array(mse_array).copy()])
    corrcoef_array.clear()
    mse_array.clear()

    for step, file_index_ in enumerate(file_hevc_result):
        data = np.array(acquire_double_linear_data(file_index_, x, y))
        corrcoef_ = np.corrcoef(souce_data, data)[0][1]
        mse_ = np.sum(np.square(data - souce_data)) / len(data)
        data = np.append(data, -1)
        data = np.append(data, corrcoef_)
        data = np.append(data, mse_)
        corrcoef_array.append(corrcoef_)
        mse_array.append(mse_)
        df3.insert(loc=0, value=np.array(data),
                   column=rename_column(crf_index[step], file_index_))
    Corrcoef_result_hevc.append([config, np.array(corrcoef_array).copy()])
    Mse_result_hevc.append([config, np.array(mse_array).copy()])
    corrcoef_array.clear()
    mse_array.clear()

    for _, file_index_ in enumerate(file_source_result):
        data = acquire_double_linear_data(file_index_, x, y)
        # watch_data(data)
        df1.insert(loc=0, value=np.array(data), column=os.path.basename(file_index_))
        if os.path.basename(file_index_)[0:36] == "a_convert_8bit_source_max_projection":
            for _ in range(3):
                data = np.append(data, -1)
            df2.insert(loc=0, value=np.array(data), column=os.path.basename(file_index_))
            df3.insert(loc=0, value=np.array(data), column=os.path.basename(file_index_))

    dfs = {'source_result': df1, 'h264_result': df2, 'hevc_result': df3}
    writer = pd.ExcelWriter(excel_filename)
    for sheet_name in dfs.keys():
        dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()


ConfigType = namedtuple('data', ['index', "position", 'point1', 'point2'])


def config_tuple():
    # ConfigType = namedtuple('data', ['index', 'point1', 'point2'])
    # my_tuple = (
    #     ConfigType('1', [190, 160], [214, 169]),
    #     ConfigType('3', [26, 264], [140, 298]),
    #     ConfigType('3', [31, 106], [36, 120]),
    #     ConfigType('4', [370, 240], [398, 244]),
    #     ConfigType('4', [494, 440], [480, 466]),
    # )

    my_tuple = [
        ConfigType('1', [200, 250], [221, 51], [300, 106]),
        ConfigType('4', [400, 450], [383, 426], [486, 348]),

    ]
    return my_tuple


def main():
    result_path = "C://Users//chenwu//Desktop//result_excel//"
    crf_index = list()
    for i in range(10, 51):
        crf_index.append(i)
    for config in config_tuple():
        draw_profile(config, crf_index, result_path)


def rand_test_demo(result_path, num=5, length=[15, 30]):
    my_tuple = []
    while len(my_tuple) < num:
        point1 = [np.random.randint(0, 511), np.random.randint(0, 511)]
        point2 = [np.random.randint(0, 511), np.random.randint(0, 511)]
        index = np.random.choice([1, 2, 3, 4, 5])
        position_left = np.random.choice([0, 50, 100, 150, 200, 250, 300, 350, 400, 450])
        position = [position_left, position_left + 50]
        tmp_config_type = ConfigType(str(index), position, point1, point2)
        real_len = calculate_line_point(point1, point2)
        if length[1] > real_len > length[0] and point2[0] != point1[0]:
            my_tuple.append(tmp_config_type)

    crf_index = list()
    for i in range(10, 51):
        crf_index.append(i)
    step = 0
    for config in my_tuple:
        try:
            draw_profile(config, crf_index, result_path)
        finally:
            step = step + 1
            print("[{}/{}] {}".format(step, num, config))
    excel_filename = result_path + "a_analyze_len_[{}_{}]_num_{}.xlsx".format(length[0], length[1], num)
    write_corrcoef_mse(excel_filename, crf_index)


def write_corrcoef_mse(excel_filename, crf_index):
    df_coef_h264 = pd.DataFrame()
    df_coef_hevc = pd.DataFrame()
    df_mse_h264 = pd.DataFrame()
    df_mse_hevc = pd.DataFrame()

    tt = [[df_coef_h264, Corrcoef_result_h264], [df_mse_h264, Mse_result_h264], [df_coef_hevc, Corrcoef_result_hevc],
          [df_mse_hevc, Mse_result_hevc]]

    for df, result_data in tt:
        tmp_data = list()
        for config, my_data in result_data:
            tmp_data.append(my_data)
            df.insert(loc=0, value=my_data,
                      column="{}_{}_{}_{}".format(config.index, config.point1, config.point2, config.position))
        df.insert(loc=0, value=np.zeros(len(crf_index)), column="0")
        df.insert(loc=0, value=np.nanmean(np.array(tmp_data), axis=0), column="mean")
        df.insert(loc=0, value=np.array(crf_index), column="CRF")
        result_data.clear()

    dfs = {'Corrcoef_result_h264': df_coef_h264, 'Mse_result_h264': df_mse_h264, 'Corrcoef_result_hevc': df_coef_hevc,
           'Mse_result_hevc': df_mse_hevc}
    writer = pd.ExcelWriter(excel_filename)
    for sheet_name in dfs.keys():
        dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)

    writer.save()


if __name__ == '__main__':
    result_path = "C://Users//chenwu//Desktop//result_excel//"

    length = [20, 200]
    num = [2000, 6000, 10000, 20000, 30000]
    for num_index_ in num:
        file = result_path + "[{},{}]_num_{}//".format(length[0], length[1], num_index_)
        os.makedirs(file)
        rand_test_demo(file, num=num_index_, length=length)

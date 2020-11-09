from utils.define_file_path import gather_file_name
from utils.calculate_coordinate import calculate_coordinate_double_linear, calculate_floor_coordinate
from utils.acquire_im_data import acquire_line_data, acquire_double_linear_data
from utils.utils_common import rename_column,watch_data
import pandas as pd
import os
import numpy as np


def draw_profile(excel_filename, file_index, crf_index, point1, point2):
    x, y = calculate_coordinate_double_linear(point1, point2)
    file_source_result, file_h264_result, file_hevc_result = gather_file_name(file_index, crf_index)

    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    df3 = pd.DataFrame()

    for _, file_index_ in enumerate(file_source_result):
        data = acquire_double_linear_data(file_index_, x, y)
        watch_data(data)
        df1.insert(loc=0, value=np.array(data), column=os.path.basename(file_index_))

    for step, file_index_ in enumerate(file_h264_result):
        data = acquire_double_linear_data(file_index_, x, y)
        df2.insert(loc=0, value=np.array(data),
                   column=rename_column(crf_index[step], file_index_))
    for step, file_index_ in enumerate(file_hevc_result):
        data = acquire_double_linear_data(file_index_, x, y)
        df3.insert(loc=0, value=np.array(data),
                   column=rename_column(crf_index[step], file_index_))

    dfs = {'source_result': df1, 'h264_result': df2, 'hevc_result': df3}
    writer = pd.ExcelWriter(excel_filename)
    for sheet_name in dfs.keys():
        dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)

    writer.save()


def analyze_tiff_max_projection(file_index, crf_index, point1, point2, result_path):
    for file_index_ in file_index:
        excel_filename = result_path + "data_{}_crf_{}_{}.xlsx".format(file_index_, crf_index[0], crf_index[-1])
        draw_profile(excel_filename, file_index_, crf_index, point1, point2)


def test_a_tiff():
    point1 = [12, 12]
    point2 = [265, 265]
    point1[0], point1[1], point2[0], point2[1] = 361, 330, 385, 330
    file_index_ = "F://Learning//Duankong//Doing//CompressTdata//data//test_result//1//a_convert_8bit_source_max_projection.tif"
    x, y = calculate_coordinate_double_linear(point1, point2)
    data = acquire_double_linear_data(file_index_, x, y)
    for step, _ in enumerate(data):
        print(" {} {} ".format(step, data[step]))


if __name__ == '__main__':
    result_path = ""
    point1 = [12, 12]
    point2 = [265, 265]
    point1[0], point1[1], point2[0], point2[1] = 15,25,26,32
    file_index = [1]
    crf_index = [17]
    analyze_tiff_max_projection(file_index, crf_index, point1, point2, result_path)

from utils.define_file_path import gather_file_name
from utils.calculate_coordinate import calculate_coordinate_double_linear, calculate_floor_coordinate
from utils.acquire_im_data import acquire_line_data, acquire_double_linear_data
from utils.utils_common import rename_column
import pandas as pd
import os
import numpy as np


def draw_profile(excel_filename, file_index, crf_index, point1, point2):
    x, y = calculate_coordinate_double_linear(point1, point2)
    file_source_result, file_h264_result, file_hevc_result = gather_file_name(file_index, crf_index)

    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    df3 = pd.DataFrame()

    for file_index_ in [file_source_result, file_h264_result, file_hevc_result]:
        print(file_index_)

    for _, file_index_ in enumerate(file_source_result):
        data = acquire_double_linear_data(file_index_, x, y)
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


if __name__ == '__main__':
    excel_filename = 'NamesAndAges.xlsx'
    point1 = [12, 12]
    point2 = [265, 265]
    file_index_ = 2
    crf_index = [17, 18]
    draw_profile(excel_filename, file_index_, crf_index, point1, point2)

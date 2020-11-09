def gather_file_name(file_index_, crf_index):
    project_path = 'F://Learning//Duankong//Doing//'
    result_path = project_path + "CompressTdata//data//test_result//"
    file_h264_result = list()
    file_hevc_result = list()
    file_souce_result = list()

    souce_8bit_file = '{}{}//a_convert_8bit_source_max_projection.tif'.format(result_path, file_index_)
    file_souce_result.append(souce_8bit_file)
    souce_16bit_file = '{}{}//a_data_souce_16bit_max_projection.tif'.format(result_path, file_index_)
    file_souce_result.append(souce_16bit_file)
    for _, crf_index_ in enumerate(crf_index):
        crf_h264_file = '{}{}//crf_{}//decode_8bit_3d_h264_max_projection.tif'.format(result_path, file_index_,
                                                                                      crf_index_)
        file_h264_result.append(crf_h264_file)
        crf_hevc_file = '{}{}//crf_{}//decode_8bit_3d_hevc_max_projection.tif'.format(result_path, file_index_,
                                                                                      crf_index_)
        file_hevc_result.append(crf_hevc_file)
    return file_souce_result, file_h264_result, file_hevc_result


if __name__ == '__main__':
    pass

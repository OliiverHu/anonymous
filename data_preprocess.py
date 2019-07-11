from rawfile_parser import file_parser
from tool_packages import get_mhd_path
from img_seg import image_segmentor
import numpy as np


def raw_reader(path, i):
    """
    :param path: path to mhd file
            i: the id of slice in raw file
    :return: a 5 channel numpy array
    """
    masked_img, file_name, origin, spacing, slice_num, width, height = image_segmentor(path, i)
    five_channels = np.array(masked_img).transpose((1, 2, 0))
    # for i in range(2, slice_num - 2, 1):
    # five_channels = np.zeros([width, height, 5])

    # for j in range(5):
    #     for x in range(width):
    #         for y in range(height):
    #             five_channels[x][y][j] = masked_img[j][x][y]

    return five_channels


def label_generation():
    linux_dir_path = ['/home/huyunfei/ct_scan/ct_data/train_part1/', '/home/huyunfei/ct_scan/ct_data/train_part2/',
                      '/home/huyunfei/ct_scan/ct_data/train_part3/', '/home/huyunfei/ct_scan/ct_data/train_part4/',
                      '/home/huyunfei/ct_scan/ct_data/train_part5/']

    win_dir_path = ['E:/tianchi-chestCT/chestCT_round1/train_part1/']

    annotation_path = '/home/huyunfei/ct_scan/chestCT_round1_annotation.csv'
    out_dir = '/home/huyunfei/ct_scan/processed_data/'

    mhd_path_list = []
    for path in linux_dir_path:
        tmp = get_mhd_path(path)
        mhd_path_list += tmp

    file_parser(mhd_path_list, annotation_path, out_dir)


if __name__ == '__main__':
    # label_generation()
    raw_reader('?', 1)

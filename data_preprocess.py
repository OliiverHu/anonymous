from rawfile_parser import file_parser
from tool_packages import get_mhd_path

linux_dir_path = ['/home/huyunfei/ct_scan/ct_data/train_part1/', '/home/huyunfei/ct_scan/ct_data/train_part2/',
                  '/home/huyunfei/ct_scan/ct_data/train_part3/', '/home/huyunfei/ct_scan/ct_data/train_part4/',
                  '/home/huyunfei/ct_scan/ct_data/train_part5/']

annotation_path = '/home/huyunfei/ct_scan/chestCT_round1_annotation.csv'
out_dir = '/home/huyunfei/ct_scan/processed_data/'

mhd_path_list = []
for path in linux_dir_path:
    tmp = get_mhd_path(path)
    mhd_path_list += tmp

file_parser(mhd_path_list, annotation_path, out_dir)

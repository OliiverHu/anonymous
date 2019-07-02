import csv
import pickle
import os
import SimpleITK as sitk
import numpy as np
from tran_mm_pix import mm2pix


# input: mhd_dir为mhd文件所在文件夹地址
# output: mhd_paths为一个包含所有mhd文件地址的list，
# 可直接用for mhd_path in mhd_paths:读取
def get_mhd_path(mhd_dir):
    mhd_paths = []

    if os.path.isdir(mhd_dir):
        for inp_file in os.listdir(mhd_dir):
            mhd_paths += [mhd_dir + inp_file]
    else:
        mhd_paths += [mhd_dir]

    mhd_paths = [inp_file for inp_file in mhd_paths if (inp_file[-4:] in ['.mhd'])]

    return mhd_paths





# 以下内容未使用
def parse_csv_annotation(ann_dir, img_dir, cache_name, labels=[]):
    if os.path.exists(cache_name):
        with open(cache_name, 'rb') as handle:
            cache = pickle.load(handle)
        all_insts, seen_labels = cache['all_insts'], cache['seen_labels']
    else:
        all_insts = []
        seen_labels = {}
        img = {'object': []}

        # for ann in sorted(os.listdir(ann_dir)):
        ann = ann_dir

        try:
            with open(ann) as f:
                # 创建cvs文件读取器
                reader = csv.reader(f)
                row_count = 0
                for row in reader:
                    row_count += 1
                    img = {'object': []}
                    file_name = row[0]
                    img['filename'] = img_dir + file_name + '.mhd'
                    if not os.path.exists(img['filename']):
                        continue
                    # if 'width' in elem.tag:
                    #     img['width'] = int(elem.text)
                    # if 'height' in elem.tag:
                    #     img['height'] = int(elem.text)
                    obj = {}
                    obj['name'] = row[7]

                    if obj['name'] in seen_labels:
                        seen_labels[obj['name']] += 1
                    else:
                        seen_labels[obj['name']] = 1

                    if len(labels) > 0 and obj['name'] not in labels:
                        pass
                    else:
                        img['object'] += [obj]

                    data = sitk.ReadImage(img['filename'])
                    origin = np.array(data.GetOrigin())  # x,y,z  Origin in world coordinates (mm)
                    spacing = np.array(data.GetSpacing())  # spacing of voxels in world coor. (mm)
                    point0 = row[1:4]
                    whl = row[4:7]
                    obj['point0'], obj['whl'] = mm2pix(point0, whl, origin, spacing)
                    # points = tran_data(obj['point0'], obj['whl'])
                    # print(points)

                    if len(img['object']) > 0:
                        all_insts += [img]

                    # if file_name == '318818':
                    #     print('318818')
                    #     print(obj['point0'])
                    #     print(obj['whl'])

                print(row_count)

                # cache = {'all_insts': all_insts, 'seen_labels': seen_labels}
                # with open(cache_name, 'wb') as handle:
                #     pickle.dump(cache, handle, protocol=pickle.HIGHEST_PROTOCOL)

        except Exception as e:
            print(e)
            print('Ignore this bad annotation: ' + ann_dir + ann)
            return

    return all_insts, seen_labels



if __name__ == '__main__':
    filename = "chestCT_round1_annotation.csv"
    mhd_path = "E:/Training/chestCT/test/"

    insts, see_labels = parse_csv_annotation(filename, mhd_path, "E/xxx", ['1', '5', '31', '32'])
    print(see_labels)

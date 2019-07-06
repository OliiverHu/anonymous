import cv2
import numpy as np
import tool_packages
from matplotlib import pyplot as plt


mhd_dir = 'chestCT_round1/test'
samples = ['chestCT_round1/test/318818.mhd']


def file_parser(mhdfile_path_list):
    for path in mhdfile_path_list:
        file_name = tool_packages.get_filename(path)
        img_set, origin, spacing = tool_packages.load_itk_image(path)
        slice_num, width, height = img_set.shape
        for i in range(2, slice_num-2, 1):
            five_channels = np.zeros([width, height, 5])
            for j in range(5):
                for x in range(width):
                    for y in range(height):
                        five_channels[x][y][j] = np.squeeze(img_set[i - 2 + j, ...])[x][y]

            np.save(file_name + '_slice' + str(i-2) + 'to' + str(i+2) + '.npy', five_channels)


def npy_tensor_loader(npy_file_path):
    test_3d_tensor = np.load(npy_file_path)
    plt.figure()
    plt.subplot(2, 3, 1), plt.imshow(test_3d_tensor[:, :, 0], 'gray'), plt.title('')
    plt.subplot(2, 3, 2), plt.imshow(test_3d_tensor[:, :, 1], 'gray'), plt.title('')
    plt.subplot(2, 3, 3), plt.imshow(test_3d_tensor[:, :, 2], 'gray'), plt.title('')
    plt.subplot(2, 3, 4), plt.imshow(test_3d_tensor[:, :, 3], 'gray'), plt.title('')
    plt.subplot(2, 3, 5), plt.imshow(test_3d_tensor[:, :, 4], 'gray'), plt.title('')
    plt.show()
    # cv2.imshow('', test_3d_tensor[:, :, 0])
    # cv2.waitKey()
    # cv2.imshow('', test_3d_tensor[:, :, 1])
    # cv2.waitKey()
    return None


# file_parser(samples)
npy_tensor_loader('318818_slice0to4.npy')

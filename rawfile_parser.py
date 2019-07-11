import img_seg
from label_parser import label_parser
import numpy as np
from matplotlib import pyplot as plt


def file_parser(mhdfile_path_list, anno_path, out_path):
    """
    :Function a raw format file parser, to generate npy files and corresponding labels for dl training
    :param mhdfile_path_list: a list of mhd file path
            anno_path: path to the annotation file
    :return: None
    """
    for path in mhdfile_path_list:
        masked_img, file_name, origin, spacing, slice_num, width, height = img_seg.image_segmentor(path)
        # masked images
        for i in range(2, slice_num-2, 1):
            five_channels = np.zeros([width, height, 5])
            for j in range(5):
                for x in range(width):
                    for y in range(height):
                        five_channels[x][y][j] = masked_img[i - 2 + j][x][y]

            np.save(out_path + file_name + '_slice' + str(i-2) + 'to' + str(i+2) + '.npy', five_channels)
            label_parser(out_path + file_name, anno_path, origin, spacing, i)


def npy_tensor_loader(npy_file_path):
    """
    Testing the parser module functionality
    :param npy_file_path:
    :return: None
    """
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


if __name__ == '__main__':
    mhd_dir = 'chestCT_round1/test'
    samples = ['chestCT_round1/test/318818.mhd']
    file_parser(samples, 'chestCT_round1_annotation.csv', 'chestCT_round1/test/')
    # npy_tensor_loader('318818_slice0to4.npy')

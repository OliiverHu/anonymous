import cv2
import numpy as np
import tool_packages
from matplotlib import pyplot as plt
from skimage.measure import label
import random


mhd_dir = 'E:/tianchi-chestCT/chestCT_round1/train_part1/'
annotation_path = 'chestCT_round1_annotation.csv'


def binary_img_reverse(binary_img):
    """
    :param binary_img:  binary image
    :return: a reversed binary image
    """
    h, w = binary_img.shape
    for i in range(w):
        for j in range(h):
            binary_img[i][j] = 1 - binary_img[i][j]

    return binary_img


def largest_connect_area(binary_img):
    """
    Utility: return the largest Connect area of a labeled image
    Parameters: binary_img: binary image
    """

    labeled_img, num = label(binary_img, neighbors=4, background=0, return_num=True)
    # plt.figure(), plt.imshow(labeled_img, 'gray')

    max_label = 0
    max_num = 0
    for i in range(1, num):  # 这里从1开始，防止将背景设置为最大连通域
        if np.sum(labeled_img == i) > max_num:
            max_num = np.sum(labeled_img == i)
            max_label = i
    lca = (labeled_img == max_label)
    # print(lca)
    return lca


def random_sampling(dir_path):
    """
    :param dir_path: path to mhd file directory
    :return: randomly selected samples from the directory pool
    """
    mhd_path_list = tool_packages.get_mhd_path(dir_path)
    sample_count = int(len(mhd_path_list) / 20)
    # sample_count = 1
    sampling = random.sample(mhd_path_list, sample_count)
    return sampling


def whole_hist_viz(image, max_thres, min_thres, name, slice_id):
    """
    histogram drawing for each slice to determine the suitable threshold
    for segmentation
    """
    MIN_BOUND = -1000
    MAX_BOUND = 800
    if max_thres < MAX_BOUND:
        MAX_BOUND = max_thres
    if min_thres > MIN_BOUND:
        MIN_BOUND = min_thres
    image[image > MAX_BOUND] = MAX_BOUND
    image[image < MIN_BOUND] = MIN_BOUND
    plt.hist(image.ravel(), max_thres - min_thres, [min_thres, max_thres], density=True)
    plt.title(name + '_slice' + slice_id, fontsize='large', fontweight='bold')
    plt.show()


def img_windowing(image, max_thres, min_thres):
    # normalize pixels to 0 ~ 1
    MIN_BOUND = -1000.0
    MAX_BOUND = 800.0
    if max_thres < MAX_BOUND:
        MAX_BOUND = max_thres
    if min_thres > MIN_BOUND:
        MIN_BOUND = min_thres
    image[image > MAX_BOUND] = MAX_BOUND
    image[image < MIN_BOUND] = MIN_BOUND
    image = np.uint8((image - MIN_BOUND) / (MAX_BOUND - MIN_BOUND) * 255)
    _, seg_thres = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # print(image.dtype)
    return image, seg_thres


def image_masked(img_mask, img):
    """
    :param img_mask: a binary mask to hide the background
    :param img: raw image
    :return: a background-masked image
    """
    # print(img)
    # print(img_mask)
    for i in range(len(img_mask)):
        for j in range(len(img_mask[0])):
            if img_mask[i][j] is img_mask[0][0]:
                img[i][j] = 0
            else:
                pass
    masked_image = img

    return masked_image


def image_segmentor(mhdfile_path):
    """
    Utility: image segmentation for lung CT scan,
    params:
        mhdfile_path -> the path to mhd file
    returns:
        mask array
    """
    # mhd_path = path_to_file
    file_name = tool_packages.get_filename(mhdfile_path)
    img_set, origin, spacing = tool_packages.load_itk_image(mhdfile_path)
    slice_num, width, height = img_set.shape
    rt = []
    # print(slice_num)
    for i in range(slice_num):
        image = np.squeeze(img_set[i, ...])

        max_pixel_value = image.max()
        min_pixel_value = image.min()

        # whole_hist_viz(image, max_pixel_value, min_pixel_value, file_name, str(i))
        image, segment_threshold = img_windowing(image, max_pixel_value, min_pixel_value)

        im2, contours, _ = cv2.findContours(segment_threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        opening = cv2.morphologyEx(segment_threshold, cv2.MORPH_OPEN, kernel)
        # closing = cv2.morphologyEx(segment_threshold, cv2.MORPH_CLOSE, kernel)

        lca = largest_connect_area(opening)
        reversed_lca = largest_connect_area(binary_img_reverse(lca))
        # print(reversed_lca)
        # print(reversed_lca[256][256])
        # mask = binary_img_reverse(reversed_lca)
        result = image_masked(reversed_lca, image)
        # print(result)
        # print(result[256][256])
        # print(lca)
        """
        plt visualization below
        """
        # plt.figure()
        # plt.subplot(2, 2, 1), plt.imshow(reversed_lca, 'gray'), plt.title('reversed_lca')
        # plt.subplot(2, 2, 2), plt.imshow(result, 'gray'), plt.title('result')
        # plt.subplot(2, 2, 3), plt.imshow(opening, 'gray'), plt.title('opening')
        # plt.subplot(2, 2, 4), plt.imshow(lca, 'gray'), plt.title('lca')
        # plt.show()
        rt.append(result)

    return rt, file_name, origin, spacing, slice_num, width, height


# samples = random_sampling(mhd_dir)
# print(samples)
if __name__ == '__main__':
    samples = 'chestCT_round1/test/318818.mhd'
    result = image_segmentor(samples)
    plt.figure()
    plt.subplot(2, 2, 1), plt.imshow(result[0], 'gray'), plt.title('test1')
    plt.subplot(2, 2, 2), plt.imshow(result[5], 'gray'), plt.title('test2')
    plt.subplot(2, 2, 3), plt.imshow(result[10], 'gray'), plt.title('test3')
    plt.subplot(2, 2, 4), plt.imshow(result[15], 'gray'), plt.title('test4')
    plt.show()


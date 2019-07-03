import csv
import SimpleITK as sitk
import matplotlib.pyplot as plt
import numpy as np
from tran_mm_pix import get_8_point
import cv2

path = 'chestCT_round1/test/318818.mhd'


def get_label_coords(csv_file, name):  # to get the label info in csv file
    labels = np.zeros((50, 8), dtype=float)
    temp_count = -1
    for i in range(len(csv_file)):
        if csv_file[i][0] == name:
            temp_count += 1
            for j in range(len(csv_file[i])):
                labels[temp_count][j] = csv_file[i][j]
        else:
            pass

    return labels


def read_csv(filename):  # csv file reader
    lines = []
    with open(filename, "rt") as f:
        csvreader = csv.reader(f)
        for line in csvreader:
            lines.append(line)
    return lines


def get_filename(file_path):  # get file name
    name = file_path.split('/')[-1].split('.')[0]
    return name


def load_itk_image(filename):  # itk image loader
    itkimage = sitk.ReadImage(filename)
    numpyImage = sitk.GetArrayFromImage(itkimage)
    numpyOrigin = np.array(list(itkimage.GetOrigin()))  # CT原点坐标
    numpySpacing = np.array(list(itkimage.GetSpacing()))  # CT像素间隔
    return numpyImage, numpyOrigin, numpySpacing


numpyImage, numpyOrigin, numpySpacing = load_itk_image(path)
print(numpyImage.shape)  # 维度为(slice,w,h)
# print(numpyOrigin)
# print(numpySpacing)


def voxel_diameter(diameter, spacing):
    return diameter / spacing


# 加载结节标注
anno_path = 'chestCT_round1_annotation.csv'
annos = read_csv(anno_path)
file_name = get_filename(path)
# print(len(annos)) length of the csv file is 12219
label = get_label_coords(annos, file_name)
# print(label)
for l in label:
    worldCoord = np.asarray([float(l[1]), float(l[2]), float(l[3])])
    diameter = np.asarray([float(l[4]), float(l[5]), float(l[6])])
    if float(l[1]) != 0:
        maxCoord, Coord, minCoord = get_8_point(worldCoord, diameter, numpyOrigin, numpySpacing)
        print("min coords :", minCoord)
        print("label :", str(int(l[7])))
        if maxCoord[2] == minCoord[2]:
            # print(minCoord[2])
            image = np.squeeze(numpyImage[minCoord[2], ...])  # if the image is 3d, the slice is integer

            '''
            bbox drawing with matplotlib
            '''
            # print(image)
            plt.imshow(image, cmap='gray')
            plt.gca().add_patch(plt.Rectangle(xy=(minCoord[0], minCoord[1]), width=maxCoord[0] - minCoord[0],
                                              height=maxCoord[1] - minCoord[1], edgecolor='#FF0000',
                                              fill=False, linewidth=0.5))

            plt.text(minCoord[0], minCoord[1] - 10, str(int(l[7])), size=10, family="fantasy", color="r",
                     style="italic", weight="light")
            plt.axis('on')
            plt.title(file_name + ' slice' + str(minCoord[2]), fontsize='large', fontweight='bold')
            # plt.show()
            plt.savefig(file_name + 'single_slice' + str(minCoord[2]))
            [p.remove() for p in reversed(plt.gca().patches)]
            [p.remove() for p in reversed(plt.gca().texts)]
        else:
            # for i in range(minCoord[2], maxCoord[2] + 1, 1):
            #     print(i)
            for i in range(minCoord[2], maxCoord[2]+1, 1):
                image = np.squeeze(numpyImage[i, ...])

                '''
                bbox drawing with matplotlib
                '''
                plt.imshow(image, cmap='gray')
                plt.gca().add_patch(plt.Rectangle(xy=(minCoord[0], minCoord[1]), width=maxCoord[0] - minCoord[0],
                                                  height=maxCoord[1] - minCoord[1], edgecolor='#FF0000',
                                                  fill=False, linewidth=0.5))

                plt.text(minCoord[0], minCoord[1] - 10, str(int(l[7])), size=10, family="fantasy", color="r",
                         style="italic", weight="light")
                plt.axis('on')
                plt.title(file_name + ' slice' + str(i), fontsize='large', fontweight='bold')
                # plt.show()
                plt.savefig(file_name + 'multi_slice' + str(minCoord[2]) + '_' + str(i - minCoord[2] + 1))
                [p.remove() for p in reversed(plt.gca().patches)]
                [p.remove() for p in reversed(plt.gca().texts)]



import csv
import SimpleITK as sitk
import matplotlib.pyplot as plt
import os
import numpy as np
from tran_mm_pix import get_8_point


def get_label_coords(csv_file, name):  # to get the label info in csv file
    labels = []  # np.zeros((50, 8), dtype=float)
    for row in csv_file:
        if row[0] == name:
            labels.append(row)
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
    img = sitk.GetArrayFromImage(itkimage)
    origin = np.array(list(itkimage.GetOrigin()))  # CT原点坐标
    spacing = np.array(list(itkimage.GetSpacing()))  # CT像素间隔
    return img, origin, spacing


def voxel_diameter(dmt, spacing):
    return dmt / spacing


image_paths = []
input_path = 'E:/tianchi-chestCT/chestCT_round1/train_part1/'
if os.path.isdir(input_path):
    for inp_file in os.listdir(input_path):
        image_paths += [input_path + inp_file]
else:
    image_paths += [input_path]

mhd_paths = [inp_file for inp_file in image_paths if (inp_file[-4:] in ['.mhd'])]
# 加载结节标注
anno_path = 'chestCT_round1_annotation.csv'
temp_csv = 'temp.csv'
annos = read_csv(anno_path)
for mhd_path in mhd_paths:
    file_name = get_filename(mhd_path)
    # print(len(annos)) length of the csv file is 12219
    label = get_label_coords(annos, file_name)
    print(label)
    numpyImage, numpyOrigin, numpySpacing = load_itk_image(mhd_path)
    s, w, h = numpyImage.shape  # 维度为(slice,w,h)
    if len(label) == 0:
        for i in range(s):
                image = np.squeeze(numpyImage[i, ...])
                plt.imshow(image, cmap='gray')
                plt.axis('on')
                plt.title(file_name + '_slice' + str(i), fontsize='large', fontweight='bold')
                # plt.show()
                plt.savefig(file_name + '_slice' + str(i))
    else:
        # with open(temp_csv, 'w', newline='') as csvfile:
        # writer = csv.writer(csvfile)
        label_db = []
        for l in label:
            worldCoord = np.asarray([float(l[1]), float(l[2]), float(l[3])])
            diameter = np.asarray([float(l[4]), float(l[5]), float(l[6])])

            maxCoord, _, minCoord = get_8_point(worldCoord, diameter, numpyOrigin, numpySpacing)
            if maxCoord[2] == minCoord[2]:
                label_db.append([minCoord[0], minCoord[1], maxCoord[0], maxCoord[1], minCoord[2], l[7]])
                # writer.writerow('\t')
            else:
                for i in range(minCoord[2], maxCoord[2]+1, 1):
                    label_db.append([minCoord[0], minCoord[1], maxCoord[0], maxCoord[1], i, l[7]])
                # writer.writerow('\t')

        bbox_label = label_db
        for i in range(s):
            image = np.squeeze(numpyImage[i, ...])  # if the image is 3d, the slice is integer
            for label in bbox_label:
                '''
                bbox drawing with matplotlib
                '''
                # print(label[4])
                # print(i)
                if int(label[4]) == i+1:
                    print('z')
                    plt.imshow(image, cmap='gray')
                    plt.gca().add_patch(plt.Rectangle(xy=(int(label[0]), int(label[1])), width=int(label[2]) - int(label[0]),
                                                      height=int(label[3]) - int(label[1]), edgecolor='#FF0000',
                                                      fill=False, linewidth=0.5))

                    plt.text(int(label[0]), int(label[1]) - 10, str(int(label[5])), size=10, family="fantasy", color="r",
                             style="italic", weight="light")
                else:
                    plt.imshow(image, cmap='gray')
            plt.axis('on')
            plt.title(file_name + '_slice' + str(i), fontsize='large', fontweight='bold')
            # plt.show()
            plt.savefig(file_name + '_slice' + str(i))
            [p.remove() for p in reversed(plt.gca().patches)]
            [p.remove() for p in reversed(plt.gca().texts)]

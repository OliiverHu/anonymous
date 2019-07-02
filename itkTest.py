import csv
import SimpleITK as sitk
import matplotlib.pyplot as plt
import numpy as np
import cv2

path = 'chestCT_round1_train_part1/test/318818.mhd'


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


'''
convert world coordinate to real coordinate
#########################################
HELP MODIFY THESE TWO FUNCTIONs DOWN BELOW, in order to output INTEGER result
#########################################
'''
def worldToVoxelCoord(worldCoord, origin, spacing):
    stretchedVoxelCoord = np.absolute(worldCoord - origin)
    voxelCoord = stretchedVoxelCoord / spacing
    return voxelCoord


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
        voxelCoord = worldToVoxelCoord(worldCoord, numpyOrigin, numpySpacing)
        print("center coords:", voxelCoord)
        voxelDiameter = voxel_diameter(diameter, numpySpacing)
        # print("diameter :", voxelDiameter)
        image = np.squeeze(numpyImage[int(voxelCoord[2]), ...])  # if the image is 3d, the slice is integer
        # fig = plt.figure(image)
        plt.imshow(image, cmap='gray')
        '''
        bbox drawing
        #########################################
        TO IMPLEMENT: identify the (0, 0, 0) of all images
        #########################################
        '''
        plt.gca().add_patch(plt.Rectangle(xy=(voxelCoord[0], voxelCoord[1]), width=voxelDiameter[0],
                                          height=voxelDiameter[1], edgecolor='#FF0000',
                                          fill=False, linewidth=0.5))
        plt.axis('on')
        plt.show()
        # cv2.imwrite('1.png', numpyImage)

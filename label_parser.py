import tool_packages
import coordinates_translator as translator
import numpy as np


def label_parser(file_name, annotation_path, origin_pos, spacing_interval, slice_num):
    csv_file = tool_packages.read_csv(annotation_path)
    labels = tool_packages.get_label_coords(csv_file, file_name)
    # print(labels)
    label_db = []
    for label in labels:
        world_coord = np.asarray([float(label[1]), float(label[2]), float(label[3])])
        diameter = np.asarray([float(label[4]), float(label[5]), float(label[6])])
        max_coord, _, min_coord = translator.get_8_point(world_coord, diameter, origin_pos, spacing_interval)
        if max_coord[2] == min_coord[2]:
            # print(min_coord[2])
            if min_coord[2] == slice_num+1:
                label_db.append([min_coord[0], min_coord[1], max_coord[0], max_coord[1], label[7], 0, 0])
                # print('received')
            else:
                pass
        else:
            for i in range(min_coord[2], max_coord[2]+1, 1):
                if i == slice_num+1:
                    # print('received')
                    if i == min_coord[2]:
                        label_db.append([min_coord[0], min_coord[1], max_coord[0], max_coord[1], label[7], 0, 1])
                    elif i == max_coord[2]+1:
                        label_db.append([min_coord[0], min_coord[1], max_coord[0], max_coord[1], label[7], 1, 0])
                    else:
                        label_db.append([min_coord[0], min_coord[1], max_coord[0], max_coord[1], label[7], 1, 1])
                else:
                    pass

    header = 'obj ' + 'xmin ymin xmax ymax ' + 'inferior superior ' + 'class '
    file = open(file_name + '_slice' + str(slice_num-2) + 'to' + str(slice_num+2) + '.txt', 'a')
    file.write(file_name + '.npy')
    file.write('\n')
    file.write(header)
    file.write('\n')
    if len(label_db) == 0:
        file.write('0')
    else:
        flag = 1
        for label in label_db:
            file.write(str(flag) + ' ')
            file.write(str(label[0]) + ' ' + str(label[1]) + ' ' + str(label[2]) + ' ' + str(label[3]) + ' ' +
                       str(label[5]) + ' ' + str(label[6]) + ' ' + str(label[4]))
            file.write('\n')
            flag += 1

    file.close()
    return None


if __name__ == '__main__':
    img_set, origin, spacing = tool_packages.load_itk_image('chestCT_round1/test/318818.mhd')
    slices, width, height = img_set.shape
    name = tool_packages.get_filename('chestCT_round1/test/318818.mhd')
    anno_path = 'chestCT_round1_annotation.csv'
    label_parser(name, anno_path, origin, spacing, 3)

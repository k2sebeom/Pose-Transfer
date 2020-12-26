import numpy as np
import pandas as pd 
import json
import os
import sys


MISSING_VALUE = -1
# fix PATH
mode = sys.argv[1]
ann_mode = 'fasion'
if len(sys.argv) > 2:
    ann_mode = sys.argv[2]

annotations_file = f'{ann_mode}-resize-annotation-{mode}.csv'
save_path = f'{mode}K'


def load_pose_cords_from_strings(y_str, x_str):
    y_cords = json.loads(y_str)
    x_cords = json.loads(x_str)
    return np.concatenate([np.expand_dims(y_cords, -1), np.expand_dims(x_cords, -1)], axis=1)


def cords_to_map(cords, img_size, sigma=6):
    result = np.zeros(img_size + cords.shape[0:1], dtype='uint8')
    for i, point in enumerate(cords):
        if point[0] == MISSING_VALUE or point[1] == MISSING_VALUE:
            continue
        xx, yy = np.meshgrid(np.arange(img_size[1]), np.arange(img_size[0]))
        result[..., i] = np.exp(-((yy - point[0]) ** 2 + (xx - point[1]) ** 2) / (2 * sigma ** 2))
        # result[..., i] = np.where(((yy - point[0]) ** 2 + (xx - point[1]) ** 2) < (sigma ** 2), 1, 0)
    return result


def compute_pose(image_dir, annotations_file, savePath):
    annotations_file = pd.read_csv(annotations_file, sep=':')
    annotations_file = annotations_file.set_index('name')
    image_size = (256, 176)
    cnt = len(annotations_file)
    for i in range(cnt):
        row = annotations_file.iloc[i]
        name = row.name
        print('processing %d / %d ... %s %s %s' %(i, cnt, savePath, name, " " * 10), end='\r')
        file_name = os.path.join(savePath, name + '.npy')
        kp_array = load_pose_cords_from_strings(row.keypoints_y, row.keypoints_x)
        pose = cords_to_map(kp_array, image_size)
        np.save(file_name, pose)
        # input()


# compute_pose(img_dir, annotations_file, save_path)
compute_pose('.', annotations_file, save_path)

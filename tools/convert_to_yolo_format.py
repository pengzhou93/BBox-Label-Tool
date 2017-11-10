# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 14:55:43 2015

This script is to convert the txt annotation files to appropriate format needed by YOLO 

@author: Guanghan Ning
Email: gnxr9@mail.missouri.edu
"""

import os
from os import walk, getcwd
from PIL import Image

classes = ["face"]


def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


"""-------------------------------------------------------------------"""

""" Configure Paths"""
image_list_file = 'wider_face/testLabels/train.txt'
label_path = "wider_face/testLabels"
out_path = "wider_face/testImagesYolo"
if not os.path.exists(out_path):
    os.mkdir(out_path)
out_image_list_file = 'train_yolo.txt'
out_image_list_f = open(os.path.join(out_path, out_image_list_file), 'w')

with open(image_list_file) as image_list_f:
    for image_path in image_list_f:
        out_image_list_f.write(image_path)
        image = Image.open(image_path.strip('\n'))
        w = int(image.size[0])
        h = int(image.size[1])

        # save in the same dir as images
        label_out_path, _ = os.path.splitext(image_path)
        out_label_file = label_out_path + '.txt'
        # out_label_file = os.path.join(out_path, title + '.txt')
        out_label_f = open(out_label_file, 'w')
        title, ext = os.path.splitext(os.path.basename(image_path))
        label_file = os.path.join(label_path, title + '.txt')
        with open(label_file) as label_f:
            label_string = ''
            for line in label_f.readlines():
                line = line.strip('\n')
                if len(line) >= 2:
                    elems = line.split(' ')
                    xmin = elems[0]
                    xmax = elems[2]
                    ymin = elems[1]
                    ymax = elems[3]
                    cls_id = elems[4]
                    b = (float(xmin), float(xmax), float(ymin), float(ymax))
                    bb = convert((w, h), b)
                    label_string += str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n'
            label_string = label_string.strip('\n')
            out_label_f.write(label_string)
        out_label_f.close()
out_image_list_f.close()


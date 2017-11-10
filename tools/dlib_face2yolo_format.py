import sys
import os
import cv2
from os import walk, getcwd
from PIL import Image
import xml.etree.ElementTree as ET
from tqdm import tqdm
import numpy as np

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


wider_face_label_files = ['dlib_face/faces_2016_09_30.xml']

wider_face_images_dirs = ['dlib_face']

out_image_list_file = 'dlib_face/dlib_face_image_list.txt'
out_image_list_f = open(out_image_list_file, 'w')
for wider_face_label_file, wider_face_images_dir in zip(wider_face_label_files, wider_face_images_dirs):
    tree = ET.parse(wider_face_label_file)
    root = tree.getroot()
    images = root.find("images")
    num_images = len(images._children)
    line_count = 0
    for image in tqdm(images.iter("image")):
        line_count += 1
        if image.find("box") == None:
            continue
        imgDir = image.get("file")
        img_path = os.path.abspath(os.path.join(wider_face_images_dir, imgDir))

        img = Image.open(img_path)

        w = int(img.size[0])
        h = int(img.size[1])

        label_string = ''
        # save in the same dir as images
#        out_label_file = out_label_file.replace('.jpg', '.txt')
#        out_label_file = out_label_file.replace('.png', '.txt')
#        out_label_file = out_label_file.replace('.JPEG', '.txt')

        result_dir = os.path.dirname(img_path)
        result_name = os.path.join(result_dir, '%06d.png'%line_count)
        result = Image.fromarray(np.array(img))
        result.save(result_name)
        out_image_list_f.write(result_name + '\n')

        label_out_path, _ = os.path.splitext(result_name)
        out_label_file = label_out_path + '.txt'
        # replace images with labels
        out_label_file = out_label_file.replace('/images/', '/labels/')
        out_label_file_dir = os.path.dirname(out_label_file)
        if not os.path.exists(out_label_file_dir):
            os.makedirs(out_label_file_dir)
        out_label_f = open(out_label_file, 'w')

        for box in image.findall("box"):
            top = int(box.attrib.get("top"))
            left = int(box.attrib.get("left"))
            width = int(box.attrib.get("width"))
            height = int(box.attrib.get("height"))
            ignore = box.attrib.get("ignore")
            if left < 0:
                left = 0
            if top < 0:
                top = 0
            if width < 0:
                width = 0
            if height < 0:
                height = 0
            x1 = float(left)
            y1 = float(top)
            width = float(width)
            height = float(height)
            cls_id = '0'
            b = (x1, x1 + width, y1, y1 + height)
            bb = convert((w, h), b)
            label_string += str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n'

        label_string = label_string.strip('\n')
        out_label_f.write(label_string)
        out_label_f.close()
        sys.stdout.write('Procuded [%d/%d]\n' % (line_count, num_images))

out_image_list_f.close()


import sys
import os
import cv2
from os import walk, getcwd
from PIL import Image


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


wider_face_label_files = ['wider_face/wider_face/wider_face_split/wider_face_train_bbx_gt.txt',
                          'wider_face/wider_face/wider_face_split/wider_face_val_bbx_gt.txt']
wider_face_images_dirs = ['wider_face/wider_face/WIDER_train/images',
                          'wider_face/wider_face/WIDER_val/images']

out_image_list_file = 'wider_face/wider_face/wider_face_image_list.txt'
out_image_list_f = open(out_image_list_file, 'w')
for wider_face_label_file, wider_face_images_dir in zip(wider_face_label_files, wider_face_images_dirs):
    with open(wider_face_label_file) as wider_face_label_f:
        content = wider_face_label_f.read().splitlines()
        line_count = 0
        while line_count < len(content):
            img_file = content[line_count]
            line_count += 1
            img_path = os.path.join(wider_face_images_dir, img_file)
            out_image_list_f.write(os.path.abspath(img_path) + '\n')
            image = Image.open(img_path)
            # debug
            # tmp_img = cv2.imread(img_path)

            w = int(image.size[0])
            h = int(image.size[1])
            num_faces = int(content[line_count])
            line_count += 1

            label_string = ''
            # save in the same dir as images
            label_out_path, _ = os.path.splitext(img_path)
            out_label_file = label_out_path + '.txt'
            # replace images with labels
            out_label_file = out_label_file.replace('/images/', '/labels/')
            out_label_file_dir = os.path.dirname(out_label_file)
            if not os.path.exists(out_label_file_dir):
                os.makedirs(out_label_file_dir)
            out_label_f = open(out_label_file, 'w')
            bbox_label = content[line_count:(line_count + num_faces)]
            line_count += num_faces
            for bbox in bbox_label:
                elems = bbox.split(' ')
                x1 = float(elems[0])
                y1 = float(elems[1])
                width = float(elems[2])
                height = float(elems[3])
                cls_id = '0'

                # debug
                # cv2.rectangle(tmp_img, (int(x1), int(y1)), (int(x1)+int(width), int(y1)+int(height)), (255, 0, 0), 2)

                b = (x1, x1+width, y1, y1+height)
                bb = convert((w, h), b)
                label_string += str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n'
            label_string = label_string.strip('\n')
            out_label_f.write(label_string)
            out_label_f.close()
            sys.stdout.write('Procuded [%d/%d]\n'%(line_count, len(content)))

            # cv2.imshow("lalala", tmp_img)
            # k = cv2.waitKey(0)  # 0==wait forever
out_image_list_f.close()

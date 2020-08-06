# -*- coding: utf-8 -*-
# @Time    : 2020/8/5 下午11:58
# @Author  : Xie
# @File    : txt_label_to_VOC.py
# @Discription : transform the UA-DETRAC txt label file to VOC xml label files

import os
import sys
import cv2
from itertools import islice
from xml.dom.minidom import Document
import matplotlib.image as pimg
import matplotlib.pyplot as plt
import numpy as np
from utils import intersect, union, area

image_label_save_rootpath = '/media/xwq/Elements/Downloads/UA-DETRAC-Dataset/UA-DETRAC/VOC2007'
labels = 'label'
image_path = 'JPEGImages/'
xml_file_path = 'Annotations/'
foldername = 'VOC2007'

images_root_path = '/media/xwq/Elements/Downloads/UA-DETRAC-Dataset/UA-DETRAC/DETRAC-train-data/Insight-MVT_Annotation_Train/'
gt_label_file_path = '/media/xwq/Elements/Downloads/UA-DETRAC-Dataset/UA-DETRAC/train_gt.txt'
ignore_bbox_file_path = '/media/xwq/Elements/Downloads/UA-DETRAC-Dataset/UA-DETRAC/train_ign.txt'



def insertObject(doc, datas):
    """insert object bbox to xml file

      Args:
        doc: xml document .
        datas: the list axies of one bbox.

      Returns:
        obj: bbox object of xml file.
    """
    obj = doc.createElement('object')
    name = doc.createElement('name')
    name.appendChild(doc.createTextNode('car'))
    obj.appendChild(name)
    pose = doc.createElement('pose')
    pose.appendChild(doc.createTextNode('Unspecified'))
    obj.appendChild(pose)
    truncated = doc.createElement('truncated')
    truncated.appendChild(doc.createTextNode(str(0)))
    obj.appendChild(truncated)
    difficult = doc.createElement('difficult')
    difficult.appendChild(doc.createTextNode(str(0)))
    obj.appendChild(difficult)
    bndbox = doc.createElement('bndbox')

    xmin = doc.createElement('xmin')
    xmin.appendChild(doc.createTextNode(str(int(datas[0]))))
    bndbox.appendChild(xmin)

    ymin = doc.createElement('ymin')
    ymin.appendChild(doc.createTextNode(str(int(datas[1]))))
    bndbox.appendChild(ymin)
    xmax = doc.createElement('xmax')
    xmax.appendChild(doc.createTextNode(str(int(datas[2]))))
    bndbox.appendChild(xmax)
    ymax = doc.createElement('ymax')
    if '\r' == str(datas[3])[-1] or '\n' == str(datas[3])[-1]:
        data = str(datas[3])[0:-1]
    else:
        data = str(int(datas[3]))
    ymax.appendChild(doc.createTextNode(data))
    bndbox.appendChild(ymax)
    obj.appendChild(bndbox)
    return obj


def create_VOC_label_file(label_file_root_path, image_name, image_size, bboxs):
    """Creat VOC xml label files refer to bboxs

      Args:
        label_file_root_path: label file root path.
        image_name: the name of image.
        image_size: the size of image, eg: image.shape
        bboxs: the list of bbox.
      Returns:
            write VOC xml file to disk.
    """

    objIndex = 0
    for bbox in bboxs:
                objIndex += 1
                #data = data.strip('\n')
                #datas = data.split(' ')
                datas = bboxs
                if 4 != len(bbox):
                    print 'bounding box information error'
                    continue
                #pictureName = each.replace('.txt', '.jpg')
                #imageFile = imgpath + pictureName
                #img = cv2.imread(imageFile)
                #imgSize = img.shape
                if objIndex == 1:
                    xmlName = image_name.replace('.jpg', '.xml')
                    f = open(os.path.join(label_file_root_path, xmlName), "w")
                    doc = Document()
                    annotation = doc.createElement('annotation')
                    doc.appendChild(annotation)

                    folder = doc.createElement('folder')
                    folder.appendChild(doc.createTextNode(foldername))
                    annotation.appendChild(folder)

                    filename = doc.createElement('filename')
                    filename.appendChild(doc.createTextNode(image_name))
                    annotation.appendChild(filename)

                    source = doc.createElement('source')
                    database = doc.createElement('database')
                    database.appendChild(doc.createTextNode('My Database'))
                    source.appendChild(database)
                    source_annotation = doc.createElement('annotation')
                    source_annotation.appendChild(doc.createTextNode(foldername))
                    source.appendChild(source_annotation)
                    image = doc.createElement('image')
                    image.appendChild(doc.createTextNode('flickr'))
                    source.appendChild(image)
                    flickrid = doc.createElement('flickrid')
                    flickrid.appendChild(doc.createTextNode('NULL'))
                    source.appendChild(flickrid)
                    annotation.appendChild(source)

                    owner = doc.createElement('owner')
                    flickrid = doc.createElement('flickrid')
                    flickrid.appendChild(doc.createTextNode('NULL'))
                    owner.appendChild(flickrid)
                    name = doc.createElement('name')
                    name.appendChild(doc.createTextNode('idaneel'))
                    owner.appendChild(name)
                    annotation.appendChild(owner)

                    size = doc.createElement('size')
                    width = doc.createElement('width')
                    width.appendChild(doc.createTextNode(str(image_size[1])))
                    size.appendChild(width)
                    height = doc.createElement('height')
                    height.appendChild(doc.createTextNode(str(image_size[0])))
                    size.appendChild(height)
                    depth = doc.createElement('depth')
                    depth.appendChild(doc.createTextNode(str(image_size[2])))
                    size.appendChild(depth)
                    annotation.appendChild(size)

                    segmented = doc.createElement('segmented')
                    segmented.appendChild(doc.createTextNode(str(0)))
                    annotation.appendChild(segmented)
                    annotation.appendChild(insertObject(doc, bbox))
                else:
                    annotation.appendChild(insertObject(doc, bbox))
    try:
        f.write(doc.toprettyxml(indent='    '))
        f.close()
    except:
        pass



def creat_mask_VOC_labelfile():
    with open(gt_label_file_path, 'r') as f:
        gt_lines = f.readlines()
    with open(ignore_bbox_file_path, 'r') as f:
        ign_lines = f.readlines()
    plt.figure(figsize=(10, 10))
    for i in gt_lines:
        info = i.split(' ')
        img_origin = pimg.imread(images_root_path + info[0])
        img_copy = img_origin.copy()
        plt.imshow(img_copy, aspect='equal')

        ign_ = [j.strip().split(' ')[1:] for j in ign_lines if j.split(' ')[0] == info[0][:9]]
        ign_bboxs = []
        if ign_:
            ign_bboxs = [float(b) for b in ign_[0]]
            # print(ign_box)
            ign_bboxs = np.array(ign_bboxs, dtype=np.float32).reshape(-1, 4)
            for b in ign_bboxs:
                rect = plt.Rectangle((b[0], b[1]), b[2] - b[0],
                                     b[3] - b[1], fill=True,
                                     facecolor='black',
                                     linewidth=1)
                plt.gca().add_patch(rect)

                # add black mask to image
                img_copy[int(b[1]):int(b[3]), int(b[0]):int(b[2]), :] = 0

        #print (ign_bbox)
        bbox = [float(b) for b in info[1:]]
        boxes = np.array(bbox, dtype=np.float32).reshape(-1, 4)

        efficient_bboxs = []

        # judge the area_intersect of bbox and ing_bbox
        for b in boxes:
            bbox_area = area(b)
            ratio_intersect = 0.0
            area_intersect = []

            for ign_bbox in ign_bboxs:
                area_intersect.append(area(intersect(b, ign_bbox)))

            max_area_intersect = max(area_intersect)
            ratio_intersect = max_area_intersect / bbox_area

            if ratio_intersect >= 0.2:
                continue
            else:
                rect = plt.Rectangle((b[0], b[1]), b[2] - b[0],
                                     b[3] - b[1], fill=False,
                                     edgecolor=(0, 1, 0),
                                     linewidth=1)
                efficient_bboxs.append(b)
                plt.gca().add_patch(rect)

        image_new_name = info[0].split('/')[0] + '_' + info[0].split('/')[1]
        #print (efficient_bboxs)
        create_VOC_label_file(os.path.join(image_label_save_rootpath, xml_file_path), image_new_name, img_origin.shape, efficient_bboxs)

        image_save_path = os.path.join(os.path.join(image_label_save_rootpath, image_path), image_new_name)
        cv2.imwrite(image_save_path, cv2.cvtColor(img_copy, cv2.COLOR_RGB2BGR))
        plt.pause(0.01)
        plt.cla()




if __name__ == '__main__':
    creat_mask_VOC_labelfile()
    #create()

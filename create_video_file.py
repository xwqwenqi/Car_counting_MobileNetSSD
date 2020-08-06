# -*- coding: utf-8 -*-
# @Time    : 2020/8/6 下午3:55
# @Author  : Xie
# @File    : create_video_file.py
# @Discription : create the video file by images


import os
import time
import cv2
import numpy as np
import glob

import dlib
from utils import CentroidTracker, TrackableObject, Conf


images_root_path = '/media/xwq/Elements/Downloads/UA-DETRAC-Dataset/UA-DETRAC/DETRAC-train-data/Insight-MVT_Annotation_Train/MVI_40192'
os.chdir(images_root_path)
image_name_list = glob.glob('*.jpg')

video_size = (960, 540)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
writer = cv2.VideoWriter("origin_video.avi",fourcc,24,video_size)


for image_name in image_name_list:
    image = cv2.imread(os.path.join(images_root_path, image_name))
    cv2.imshow('origin images', image)
    writer.write(image)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
print ('Done!!!!')
writer.release()


#print (image_name_list)

# -*- coding: utf-8 -*-
# @Time    : 2020/8/6 下午5:38
# @Author  : Xie
# @File    : delete_xml_file.py
# @Discription :


import glob
import os

xml_file_path = '/media/xwq/Elements/Downloads/UA-DETRAC-Dataset/UA-DETRAC/VOC2007/Annotations'
image_file_path

os.chdir(xml_file_path)

xml_file_name_list = glob.glob('*.xml')
print (len(xml_file_name_list))
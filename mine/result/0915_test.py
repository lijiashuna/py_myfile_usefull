
from __future__ import division
from  .personhead_cut import head_cut_and_xml_change
import os
from PIL import Image
import xml.dom.minidom
import numpy as np
import xml.etree.ElementTree as ET
import cv2

root_imgpath = 'H:/lijiashun/tmp_0914/images'
root_annopath = 'H:/lijiashun/tmp_0914/labels'
new_imgpath = 'H:/lijiashun/tmp_0914/new_images/'
new_annopath = 'H:/lijiashun/tmp_0914/new_labels/'
for file in os.listdir(root_imgpath):
    filename,etc =os.path.splitext(file)
    imgpath = root_imgpath + '/' + file
    annopath = root_annopath +  '/' + file.replace('.jpg','.xml')
    head_cut_and_xml_change(imgpath, annopath,filename,new_imgpath,new_annopath)
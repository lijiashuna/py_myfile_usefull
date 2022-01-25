from __future__ import division
import os
from PIL import Image
import xml.dom.minidom
import numpy as np
import xml.etree.ElementTree as ET
import cv2


encoding = '<?xml version="1.0" encoding="UTF-8"?>'
prefix_str = '''<annotation>
        <folder>images</folder>
        <filename>{}.jpg</filename>
        <path>from_tongyongxingren_chengducaiji_2021_0722-0727</path>
        <size>
            <width>{}</width>
            <height>{}</height>
            <depth>3</depth>
        </size>'''

suffix = '</annotation>'

new_head = '''	<object>
        <name>head</name>
        <difficult>0</difficult>
        <bndbox>
            <xmin>{}</xmin>
            <ymin>{}</ymin>
            <xmax>{}</xmax>
            <ymax>{}</ymax>
        </bndbox>
    </object>'''

def head_cut_and_xml_change(img_filename,ann_filename,filename,new_imgpath,new_annopath):

    in_file = open( ann_filename ,encoding='utf-8')
    print(in_file)
    tree = ET.parse(in_file)
    root = tree.getroot()
    img = cv2.imread( img_filename)
    num=0
    for obj in root.iter('object'):
        image_size=[]
        namebox = obj.find('name').text
        if namebox == 'person':
            xmlbox = obj.find('bndbox')
            image_size.append(int(xmlbox.find('xmin').text))
            image_size.append(int(xmlbox.find('ymin').text))
            image_size.append(int(xmlbox.find('xmax').text))
            image_size.append(int(xmlbox.find('ymax').text))
            print(image_size)
            new_img = img[image_size[1]:image_size[3],image_size[0]:image_size[2]]
            m = image_size[2] - image_size[0]
            n = image_size[3] - image_size[1]
            bboxes = []
            for obj2 in root.iter('object'):
                toubu_size=[]
                toubu_namebox = obj2.find('name').text
                if toubu_namebox == '头部':
                    print('11111111')
                    toubu_xmlbox = obj2.find('bndbox')
                    toubu_size.append(int(toubu_xmlbox .find('xmin').text))
                    toubu_size.append(int(toubu_xmlbox .find('ymin').text))
                    toubu_size.append(int(toubu_xmlbox .find('xmax').text))
                    toubu_size.append(int(toubu_xmlbox .find('ymax').text))
                    print(toubu_size)
                    s_toubu = (toubu_size[2] - toubu_size[0])*(toubu_size[3] - toubu_size[1])
                    a = toubu_size[0] - image_size[0]
                    b = toubu_size[1] - image_size[1]
                    c = toubu_size[2] - image_size[0]
                    d = toubu_size[3] - image_size[1]
                    if a < 0:
                        a = 0
                    if a > m:
                        a = m
                    if b < 0:
                        b = 0
                    if b > n:
                        b = n
                    if c < 0:
                        c = 0
                    if c > m:
                        c = m
                    if d < 0:
                        d = 0
                    if d > n:
                        b = m
                    s_new_toubu = (c-a)*(d-b)
                    if float(s_new_toubu/s_toubu) > 0.5:
                        bboxes.append([a,b,c,d])
            print(bboxes)
            if bboxes:
                cv2.imwrite( new_imgpath + str(num) + '_' + filename + ".jpg", new_img)
                head_str = ''
                for Bbox in bboxes:
                    head_str = head_str + new_head.format(Bbox[0], Bbox[1], Bbox[2], Bbox[3])
                    xml = encoding + prefix_str.format(filename,m,n) + head_str + suffix
                    open(new_annopath + str(num) +  '_' + filename + ".xml", 'w').write(xml)
            num+=1




root_imgpath = 'H:/lijiashun/tmp_0914/images'
root_annopath = 'H:/lijiashun/tmp_0914/labels'
new_imgpath = 'H:/lijiashun/tmp_0914/new_images/'
new_annopath = 'H:/lijiashun/tmp_0914/new_labels/'
for file in os.listdir(root_imgpath):
    filename,etc =os.path.splitext(file)
    imgpath = root_imgpath + '/' + file
    annopath = root_annopath +  '/' + file.replace('.jpg','.xml')
    head_cut_and_xml_change(imgpath, annopath,filename,new_imgpath,new_annopath)
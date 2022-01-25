from __future__ import division
import os
from PIL import Image
import xml.dom.minidom
import numpy as np
import xml.etree.ElementTree as ET
import cv2

imgpath = 'H:/lijiashun/tmp_0914/images/'
annopath = 'C:/Users/yaoyao/Desktop/XML_try/xml/'
processedpath = 'C:/Users/yaoyao/Desktop/pic/'

def head_cut_and_xml_change(img_filename,ann_filename,processedpath):
    prefix_str = '''<annotation>
        <folder>images</folder>
        <filename>{}.jpg</filename>
        <path>=AWS4-HMAC-SHA256&X-Amz-Credential=NPW7ZGJH2JVEPGPCJ0JV%2F20210908%2Fdefault%2Fs3%2Faws4_request&X-Amz-Date=20210908T065702Z&X-Amz-Expires=18000&X-Amz-SignedHeaders=host&X-Amz-Signature=3f8d5cefc4f39ebc0d00cb727167d74f4f187694195b0e40ba0530f1915b1796</path>
        <size>
            <width>{}</width>
            <height>{}</height>
            <depth>3</depth>
        </size>'''

    suffix = '</annotation>'

    new_head = '''	<object>
            <name>头部</name>
            <difficult>0</difficult>
            <bndbox>
                <xmin>{}</xmin>
                <ymin>{}</ymin>
                <xmax>{}</xmax>
                <ymax>{}</ymax>
            </bndbox>
        </object>'''
    an_res = []

    in_file = open(annopath + '/' + ann_filename )
    #out_file = open(root_path1 + xml_path.replace('.xml', '.txt'), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    # size = root.find('size')
    # w = int(size.find('width').text)
    # h = int(size.find('height').text)
    img = cv2.imread(imgpath + '/' + img_filename)
    #print(img.shape)
    #cropped = img[0:128, 0:512]  # 裁剪坐标为[y0:y1, x0:x1]
    #cv2.imwrite("./data/cut/cv_cut_thor.jpg", cropped)
    for obj in root.iter('object'):
        image_size=[]
        namebox = obj.find('name').text
        if namebox == 'person':
            xmlbox = obj.find('bndbox')
            image_size.append(float(xmlbox.find('xmin').text))
            image_size.append(float(xmlbox.find('xmax').text))
            image_size.append(float(xmlbox.find('ymin').text))
            image_size.append(float(xmlbox.find('ymax').text))
            # print(tmp)
            new_img = img[image_size[2]:image_size[3],image_size[0]:image_size[1]]
            cv2.imwrite("new_img.jpg", new_img)









'''
    for image in imagelist:
        image_pre, ext = os.path.splitext(image)
        imgfile = ImgPath + image
        xmlfile = AnnoPath + image_pre + '.xml'

        DomTree = xml.dom.minidom.parse(xmlfile)  # 打开xml文档
        annotation = DomTree.documentElement  # 得到xml文档对象

        filenamelist = annotation.getElementsByTagName('filename')  # [<DOM Element: filename at 0x381f788>]
        filename = filenamelist[0].childNodes[0].data  # 获取XML节点值
        namelist = annotation.getElementsByTagName('name')
        objectname = namelist[0].childNodes[0].data
        savepath = ProcessedPath + objectname
        if not os.path.exists(savepath):
            os.makedirs(savepath)

        bndbox = annotation.getElementsByTagName('bndbox')
        b = bndbox[1]
        print(b.nodeName)
        i = 1
        a = [0, 300, 0, 300]
        b = [0, 0, 300, 300]
        h = 300
        cropboxes = []


        def select(m, n):
            bbox = []
            for index in range(0, len(bndbox)):
                x1_list = bndbox[index].getElementsByTagName('xmin')  # 寻找有着给定标签名的所有的元素
                x1 = int(x1_list[0].childNodes[0].data)
                y1_list = bndbox[index].getElementsByTagName('ymin')
                y1 = int(y1_list[0].childNodes[0].data)
                x2_list = bndbox[index].getElementsByTagName('xmax')
                x2 = int(x2_list[0].childNodes[0].data)
                y2_list = bndbox[index].getElementsByTagName('ymax')
                y2 = int(y2_list[0].childNodes[0].data)
                print("the number of the box is", index)
                print("the xy", x1, y1, x2, y2)
                if x1 >= m and x2 <= m + h and y1 >= n and y2 <= n + h:
                    print(x1, y1, x2, y2)
                    a1 = x1 - m
                    b1 = y1 - n
                    a2 = x2 - m
                    b2 = y2 - n
                    bbox.append([a1, b1, a2, b2])  # 更新后的标记框
            if bbox is not None:
                return bbox
            else:
                return 0


        cropboxes = np.array(
            [[a[0], b[0], a[0] + h, b[0] + h], [a[1], b[1], a[1] + h, b[1] + h], [a[2], b[2], a[2] + h, b[2] + h],
             [a[3], b[3], a[3] + h, b[3] + h]])
        img = Image.open(imgfile)
        for j in range(0, len(cropboxes)):
            print("the img number is :", j)
            Bboxes = select(a[j], b[j])
            if Bboxes is not 0:
                head_str = ''
                for Bbox in Bboxes:
                    head_str = head_str + new_head.format(Bbox[0], Bbox[1], Bbox[2], Bbox[3])
            cropedimg = img.crop(cropboxes[j])
            xml = prefix_str.format(image) + head_str + suffix
            cropedimg.save(savepath + '/' + image_pre + '_' + str(j) + '.jpg')
            open(AnnoPath + 'test{}.xml'.format(j), 'w').write(xml)
'''

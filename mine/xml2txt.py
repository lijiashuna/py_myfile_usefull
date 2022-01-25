import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
'''
yolo格式
sets=[('2012', 'train'), ('2012', 'val'), ('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

classes = ['person']

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(xml_path):  # 转换这一张图片的坐标表示方式（格式）,即读取xml文件的内容，计算后存放在txt文件中。
    in_file = open(root_path + '/' + xml_path)
    out_file = open(root_path1 + xml_path.replace('.xml','txt'), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()
root_path=""
root_path1=""
for year, image_set in sets:
    if not os.path.exists('VOCdevkit/VOC%s/labels/'%(year)):
        os.makedirs('VOCdevkit/VOC%s/labels/'%(year))  # 新建一个 label 文件夹，用于存放yolo格式的标签文件：000001.txt
    image_ids = open('VOCdevkit/VOC%s/ImageSets/Main/%s.txt'%(year, image_set)).read().strip().split()  # 读取txt文件中 存放的图片的 id：000001
    list_file = open('%s_%s.txt'%(year, image_set), 'w')  # 新建一个 txt文件，用于存放 图片的绝对路径：/media/common/yzn_file/DataSetsH/VOC/VOCdevkit/VOC2007/JPEGImages/000001.jpg
    for image_id in image_ids:
        list_file.write('%s/VOCdevkit/VOC%s/JPEGImages/%s.jpg\n'%(wd, year, image_id))  # 向 txt 文件中写入 一张图片的绝对路径
        convert_annotation(year, image_id)  # 转换这一张图片的坐标表示方式（格式）
    list_file.close()
    '''


'''for my xml2txt_onlypoint_nopxiel_noclass'''
def convert_annotation(xml_path):  # 转换这一张图片的坐标表示方式（格式）,即读取xml文件的内容，计算后存放在txt文件中。
    an_res=[]

    in_file = open(root_path + '/' + xml_path)
    out_file = open(root_path1 + xml_path.replace('.xml','.txt'), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    #size = root.find('size')
    #w = int(size.find('width').text)
    #h = int(size.find('height').text)

    for obj in root.iter('object'):
        tmp=[]
        #difficult = obj.find('difficult').text
        #cls = obj.find('name').text
        #if cls not in classes or int(difficult) == 1:
            #continue
        #cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        tmp.append(float(xmlbox.find('xmin').text))
        tmp.append(float(xmlbox.find('xmax').text))
        tmp.append(float(xmlbox.find('ymin').text))
        tmp.append(float(xmlbox.find('ymax').text))
        #print(tmp)
        an_res.append(tmp)
        print(an_res)
        print(len(an_res))
    return an_res
        #b = list(float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        #bb = convert((w,h), b)
        #out_file.write(str(b) + '\n')

root_path="H:/chongtai/通用模型/行人/ai-auto-test-行人检测/labels"
root_path1="E:/pycharm/pycharmtest/mine/result/"
convert_annotation('1336144930712268800.xml')
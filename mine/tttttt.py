'''error anaysis for person detection'''

import requests
import base64
import json
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
from PIL import Image, ImageDraw
from PIL import ImageFile
from torchvision.transforms import transforms
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
'''error anaysis for person detection'''
def convert_annotation(xml_path):  # 转换这一张图片的坐标表示方式（格式）,即读取xml文件的内容，计算后存放在txt文件中。
    an_res=[]
    in_file = open(label_root_path + '/' + xml_path)
    #out_file = open(root_path1 + xml_path.replace('.xml','.txt'), 'w')
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
        tmp.append(float(0))
        #print(tmp)
        an_res.append(tmp)
        #print(an_res)
        #b = list(float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        #bb = convert((w,h), b)
        #out_file.write(str(b) + '\n')
    return an_res

def rawimage_box(x,img,filename,i):
    for line in x:
        #print(line[0])
        x_top = int(line[0])

        y_top = int(line[1])

        x_bot = int(line[2])

        y_bot = int(line[3])

        line[4] = round(line[4],2)
        img = img.convert('RGB')
        draw = ImageDraw.Draw(img)
        #draw.rectangle([int(x_top), int(y_top), int(x_bot),int( y_bot)],  width = 5)
        draw.rectangle([int(x_top), int(y_top), int(x_bot), int(y_bot)])
        draw.text((x_top,y_top),str(line[4]), fill=(255, 0, 0))

    if i==0:
        img.save('H:/lijiashun/analysis/tmp/wucha/' + filename)
    elif i==1:
        img.save('H:/lijiashun/analysis/tmp/wucha/' + filename)
    else:
        img.save('H:/lijiashun/analysis/tmp/wucha/' + filename)



label_root_path="H:/chongtai/通用模型/行人/ai-auto-test-行人检测/labels"
image_root_path = 'H:/lijiashun/analysis/tmp/loujian1'
num=0
cuojian=0
loujian=0
loujian_person=0
cuojian_person=0
total_person=0


post_data = {
        'model': 'ai-auto-common-detection-person'
    }

ip = '172.31.3.250'
res = requests.post(url="http://{}:5000/init_model".format(ip), data=post_data)
print(res.text)

for filename in os.listdir(image_root_path):
    guolv_res=[]
    imgpath=image_root_path + '/'  + filename
    # img = Image.open(imgpath)
    # size = img.size
    # # img = transforms.RandomResizedCrop((int(size[1] * 0.9), int(size[0] * 0.9)))(img)
    # img = transforms.RandomCrop((int(size[1] * 0.9), int(size[0] * 0.9)))(img)
    # img.save('H:/lijiashun/analysis/tmp/tmp' + '/' + filename)
    # imgpath=crop_(imgpath)
    #file = open('H:/lijiashun/analysis/tmp/tmp' + '/' + filename, 'rb')
    file = open(imgpath , 'rb')
    data = file.read()
    encode_data = base64.b64encode(data)
    post_data = {
        'image': encode_data
    }

    res = requests.post(url="http://{}:5000/inference".format(ip), data=post_data)
    #print(res.text)
    y=json.loads(res.text)
    for item in y[0]:
        if item[4] > 0.4 :
            guolv_res.append(item)
    #print(guolv_res)
    #print(len(guolv_res))
    #阈值0.4
    xml_path=filename.replace('.jpg' , '.xml')
    res_xml=convert_annotation(xml_path)
    if len(guolv_res) < len(res_xml):
        img = Image.open(imgpath)
        # rawimage_box(guolv_res, img, filename, 0)
        img.save('H:/lijiashun/analysis/loujian_ori/' + filename)
        loujian += 1
        loujian_person += len(res_xml) - len(guolv_res)
    elif len(guolv_res) > len(res_xml):
        img = Image.open(imgpath)
        # rawimage_box(guolv_res, img, filename, 1)
        img.save('H:/lijiashun/analysis/cuojian_ori/' + filename)
        cuojian += 1
        cuojian_person += len(guolv_res) - len(res_xml)
    else:
        total_person += len(guolv_res)

    num+=1
    print("  漏检：%d  --- 漏检人数：%d    ----  错检：%d   --- 错检人数：%d   ----  遍历总数：%d  ---遍历总正确人数：%d "%(loujian,loujian_person,cuojian,cuojian_person,num,total_person))



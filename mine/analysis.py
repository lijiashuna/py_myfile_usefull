'''error anaysis for person detection'''
import cv2
import requests
import base64
import json
import xml.etree.ElementTree as ET
import pickle
import os
import random
import numpy as np
from PIL import Image, ImageDraw
from PIL import ImageFile
from torchvision.transforms import transforms
import cv2

ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
'''error anaysis for person detection'''


def convert_annotation(xml_path, size, half_crop_size):  # 读取xml标注信息并按照cropsize转换xml坐标。
    an_res = []
    in_file = open(label_root_path + '/' + xml_path)
    tree = ET.parse(in_file)
    root = tree.getroot()
    for obj in root.iter('object'):
        tmp = []
        ori = []
        xmlbox = obj.find('bndbox')
        ori.append(float(xmlbox.find('xmin').text))
        ori.append(float(xmlbox.find('xmax').text))
        ori.append(float(xmlbox.find('ymin').text))
        ori.append(float(xmlbox.find('ymax').text))
        ori_area = (ori[1] - ori[0]) * (ori[3] - ori[2])
        # print(ori)
        if float(xmlbox.find('xmin').text) - size[0] * half_crop_size > 0:
            tmp.append(float(xmlbox.find('xmin').text) - size[0] * half_crop_size)
        else:
            tmp.append(0)
        if float(xmlbox.find('xmax').text) - size[0] * half_crop_size > 0:
            tmp.append(float(xmlbox.find('xmax').text) - size[0] * half_crop_size)
        else:
            tmp.append(0)
        if float(xmlbox.find('ymin').text) - size[1] * half_crop_size > 0:
            tmp.append(float(xmlbox.find('ymin').text) - size[1] * half_crop_size)
        else:
            tmp.append(0)
        if float(xmlbox.find('ymax').text) - size[1] * half_crop_size > 0:
            tmp.append(float(xmlbox.find('ymax').text) - size[1] * half_crop_size)
        tmp_area = (tmp[1] - tmp[0]) * (tmp[3] - tmp[2])
        if tmp_area / ori_area > 0.7:
            an_res.append(tmp)

        # print(an_res)
        # print(len(an_res))
    return an_res


def rawimage_box(x, img, filename, i):
    for line in x:
        # print(line[0])
        x_top = int(line[0])

        y_top = int(line[1])

        x_bot = int(line[2])

        y_bot = int(line[3])

        line[4] = round(line[4], 2)
        img = img.convert('RGB')
        draw = ImageDraw.Draw(img)
        # draw.rectangle([int(x_top), int(y_top), int(x_bot),int( y_bot)],  width = 5)
        draw.rectangle([int(x_top), int(y_top), int(x_bot), int(y_bot)])
        draw.text((x_top, y_top), str(line[4]), fill=(255, 0, 0))

    if i == 0:
        img.save('H:/lijiashun/analysis/tmp/loujian/' + filename)
    elif i == 1:
        img.save('H:/lijiashun/analysis/tmp/cuojian/' + filename)
    else:
        img.save('H:/lijiashun/analysis/tmp/wucha/' + filename)

def RandomBrightness(bgr):
    if random.random() < 0.5:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h,s,v = cv2.split(hsv)
        adjust = random.choice([0.5,1.5])
        v = v*adjust
        v = np.clip(v, 0, 255).astype(hsv.dtype)
        hsv = cv2.merge((h,s,v))
        bgr = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    return bgr

def RandomHue(bgr):
    if random.random() < 0.5:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h,s,v = cv2.split(hsv)
        adjust = random.choice([0.5,1.5])
        h = h*adjust
        h = np.clip(h, 0, 255).astype(hsv.dtype)
        hsv = cv2.merge((h,s,v))
        bgr = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    return bgr

def random_bright(im, delta=16):
    alpha = random.random()
    if alpha > 0.3:
        im = im * alpha + random.randrange(-delta,delta)
        im = im.clip(min=0,max=255).astype(np.uint8)
    return im

label_root_path = "H:/lijiashun/analysis/labels"
image_root_path = 'H:/lijiashun/analysis/images'
# image_root_path = 'H:/lijiashun/analysis/tmp/soruce'
num = 0
cuojian = 0
loujian = 0
loujian_person = 0
cuojian_person = 0
total_person = 0

post_data = {
    'model': 'ai-auto-common-detection-person'
}

ip = '172.31.3.250'
res = requests.post(url="http://{}:5000/init_model".format(ip), data=post_data)
print(res.text)
gt_list = []
for filename in os.listdir(image_root_path):
    guolv_res = []
    imgpath = image_root_path + '/' + filename
    img1 = Image.open(imgpath)
    size = img1.size
    #img = cv2.imread(imgpath)
    #img = random_bright(img)
    #img = RandomBrightness(img)
    #print(imgpath)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # constant = cv2.copyMakeBorder(img, 100, 100, 100, 100, cv2.BORDER_CONSTANT, value=0)
    # constant = cv2.cvtColor(constant, cv2.COLOR_RGB2BGR)
    crop_imgpath = 'H:/lijiashun/analysis/tmp/tmp' + '/' + filename + '.jpg'
    #cv2.imwrite(crop_imgpath , img)
    img = Image.open(imgpath)
    img = transforms.CenterCrop((int(size[1] * 0.9), int(size[0] * 0.9)))(img)
    # crop_imgpath='H:/lijiashun/analysis/tmp/tmp' + '/' + filename
    img.save(crop_imgpath)
    # imgpath=crop_(imgpath)
    file = open(crop_imgpath, 'rb')
    data = file.read()
    encode_data = base64.b64encode(data)
    post_data = {
        'image': encode_data
    }

    res = requests.post(url="http://{}:5000/inference".format(ip), data=post_data)  # -1本地transform
    # print(res.text)
    y = json.loads(res.text)
    for item in y[0]:
        # 阈值0.4
        if item[4] > 0.5:
            guolv_res.append(item)
            # if item[4] < 0.5:
            # gt_list.append(item[4])
    # print(guolv_res)
    # print(len(guolv_res))
    # 阈值0.4
    xml_path = filename.replace('.jpg', '.xml')
    res_xml = convert_annotation(xml_path, size, 0.05)
    if len(guolv_res) < len(res_xml):
        img = Image.open(crop_imgpath)
        rawimage_box(guolv_res, img, filename, 0)
        # img.save('H:/lijiashun/analysis/loujian_ori/' + filename)
        loujian += 1
        loujian_person += len(res_xml) - len(guolv_res)
    elif len(guolv_res) > len(res_xml):
        img = Image.open(crop_imgpath)
        rawimage_box(guolv_res, img, filename, 1)
        # img.save('H:/lijiashun/analysis/cuojian_ori/' + filename)
        cuojian += 1
        cuojian_person += len(guolv_res) - len(res_xml)
    else:
        total_person += len(guolv_res)
        img = Image.open(crop_imgpath)
        rawimage_box(guolv_res, img, filename, 2)
    num += 1
    print("  漏检：%d  --- 漏检人数：%d    ----  错检：%d   --- 错检人数：%d   ----  遍历总数：%d  ---遍历正确总人数：%d " % (
        loujian, loujian_person, cuojian, cuojian_person, num, total_person))

# print(gt_list)
# 0909 漏检：1264  --- 漏检人数：2109    -----  错检：3836   --- 错检人数：8230   ----  遍历总数：14615
# 0910 漏检：3538  --- 漏检人数：6121    ----  错检：10529   --- 错检人数：22381   ----  遍历总数：40330  ---遍历总人数：59155
# 0913 漏检：22  --- 漏检人数：53    ----  错检：73   --- 错检人数：145   ----  遍历总数：300  ---遍历总人数：525  0.4
#     漏检：52  --- 漏检人数：120    ----  错检：37   --- 错检人数：63   ----  遍历总数：300  ---遍历总人数：541 0.5
#     漏检：38  --- 漏检人数：85    ----  错检：52   --- 错检人数：95    ----  遍历总数：300  ---遍历总人数：532 0.45
#     漏检：29  --- 漏检人数：66    ----  错检：63   --- 错检人数：120   ----  遍历总数：295  ---遍历正确总人数：526  0.42
#     漏检：146  --- 漏检人数：395    ---  错检：28   --- 错检人数：52   ----  遍历总数：300  ---遍历正确总人数：209    图片resizedcrop0.9
# 0914 漏检：37  --- 漏检人数：70    ----  错检：67   --- 错检人数：128   ----  遍历总数：300  ---遍历正确总人数：447  cropsize=0.9 chonghe=0.8
#     漏检：43  --- 漏检人数：79    ----  错检：58   --- 错检人数：109   ----  遍历总数：300  ---遍历正确总人数：479                       0.6
#     漏检：41  --- 漏检人数：76    ----  错检：59   --- 错检人数：112   ----  遍历总数：300  ---遍历正确总人数：481                       0.7
# 0915 漏检：70  --- 漏检人数：121    ----  错检：307   --- 错检人数：692   ----  遍历总数：1000  ---遍历正确总人数：1347    crop0.9 padding(100,100,100,100)
#     漏检：82  --- 漏检人数：147    ----  错检：263   --- 错检人数：564   ----  遍历总数：1000  ---遍历正确总人数：1524     padding(100,100,100,100)0.40
#     漏检：126  --- 漏检人数：254    ----  错检：196   --- 错检人数：368   ----  遍历总数：1000  ---遍历正确总人数：1574   padding(100,100,100,100) 0.45
#     漏检：173  --- 漏检人数：379    ----  错检：140   --- 错检人数：250   ----  遍历总数：1000  ---遍历正确总人数：1563    padding(100,100,100,100)0.50
#     漏检：170  --- 漏检人数：367    ----  错检：116   --- 错检人数：209   ----  遍历总数：1000  ---遍历正确总人数：1743   0.5
# #     漏检：130  --- 漏检人数：232    ----  错检：168   --- 错检人数：322   ----  遍历总数：1000  ---遍历正确总人数：1674   0.45
# #     漏检：82  --- 漏检人数：146    ----  错检：250   --- 错检人数：508   ----  遍历总数：1000  ---遍历正确总人数：1547   0.40
# #     漏检：222  --- 漏检人数：498    ----  错检：83   --- 错检人数：148   ----  遍历总数：1000  ---遍历正确总人数：1571    0.55
#       漏检：240  --- 漏检人数：536    ----  错检：78   --- 错检人数：136   ----  遍历总数：1000  ---遍历正确总人数：1484     Random_Brightness 0.55
#       漏检：140  --- 漏检人数：277    ----  错检：167   --- 错检人数：313   ----  遍历总数：1000  ---遍历正确总人数：1672    Random_Brightness 0.45
#       漏检：181  --- 漏检人数：403    ----  错检：104   --- 错检人数：190   ----  遍历总数：1000  ---遍历正确总人数：1705                       0.5

import xml.etree.ElementTree as ET
import sys

xml_path='E:\pycharm\pycharmtest\yolo3-pytorch-master\VOCdevkit\VOC2007\Annotations/00001.xml'
tree = ET.parse(xml_path)
rect={}
line=""
root = tree.getroot()
label=[]
with open('blog.txt','w',encoding='utf-8') as f1:
   # 路径信息
   for name in root.iter('path'):
       rect['path'] = name.text
   for ob in root.iter('object'):

       for bndbox in ob.iter('bndbox'):
           # for l in bndbox:
           #     print(l.text)
           # 坐标信息
           for xmin in bndbox.iter('xmin'):
               rect['xmin'] = xmin.text
           for ymin in bndbox.iter('ymin'):
               rect['ymin'] = ymin.text
           for xmax in bndbox.iter('xmax'):
               rect['xmax'] = xmax.text
           for ymax in bndbox.iter('ymax'):
               rect['ymax'] = ymax.text
           #print(rect['xmin']+ ' '+rect['ymin']+' '+rect['xmax']+' '+rect['ymax'])
           line = rect['xmin']+ ' '+rect['ymin']+' '+rect['xmax']+' '+rect['ymax'] + " "
           f1.write(line)
           # 文本信息
           for t in ob.iter('name'):
               print(t.text)
               f1.write(t.text + '\n')
           label.append(line + t.text)
           print(label)

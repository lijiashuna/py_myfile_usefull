from torchvision.datasets import VisionDataset
import mmcv
import os.path as osp
from PIL import Image
import torch
import xml.etree.ElementTree as ET
import sys


class MyDataset(VisionDataset):#torch.utils.data.DataLoader的前项处理函数   继承VisionDataset类
    def __init__(self, root, transform=None, target_transform=None):#定义函数输入为路径 transform和target_transform

        super(MyDataset, self).__init__(root, transform=transform,
                                           target_transform=target_transform)#获取VisionDataset的属性，并给VisionDataset类赋值

        paths = sorted(list(mmcv.scandir(self.root, recursive=True)))#mmcv.scandir可遍历提取到最底层文件信息，返回为路径列表

        self.image_paths = []
        self.labels = []
        labels = []
        for path in paths:#遍历文件路径列表
            if path.endswith('.xml') and 'Annotations' in path:#判断满足文件结尾为.json and 在labels文件夹下
                # label = mmcv.load(osp.join(self.root, path))['relationTagInfo'][0]['value']#mmcv.loadj读取json文件标注信息 返回为字典
                tree = ET.parse(osp.join(self.root, path))
                rect = {}
                line = ""
                root = tree.getroot()
                with open('blog.txt', 'w', encoding='utf-8') as f1:
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
                            #print(rect['xmin'] + ' ' + rect['ymin'] + ' ' + rect['xmax'] + ' ' + rect['ymax'])
                            line = rect['xmin'] + ' ' + rect['ymin'] + ' ' + rect['xmax'] + ' ' + rect['ymax'] + " "
                            f1.write(line)
                           # 文本信息
                            for t in ob.iter('name'):
                                #print(t.text)
                                f1.write(t.text + '\n')
                            label = [line + t.text]
                            self.labels.append((path, label))
                            labels.append(label)

            elif path.endswith('.jpg') and 'JPEGImages' in path:
                self.image_paths.append(path)
        print(self.image_paths,self.labels)
        assert len(self.image_paths) == len(self.labels)  #判断图片数量和标签数量是否一直
        for image_path, (label_path, _) in zip(self.image_paths, self.labels):
            assert osp.splitext(osp.basename(image_path))[0] == osp.splitext(osp.basename(label_path))[0]#osp.basename提取文件名
                                                                                                # osp.splitext将文件id和后缀分开

        unique_labels = [12,23,6,3,62,2,]#取出label元组
        self.name_to_label = {name: label for label, name in enumerate(unique_labels)}#将标签号和标签含义对应
        print(self.name_to_label)
        self.transform = transform
        self.target_transform = target_transform

        print('Data size {}'.format(len(self)))

        self.num_classes = len(self.name_to_label)

    def __len__(self):
        return len(self.image_paths)


    def __getitem__(self, index):#index为固定
        img = Image.open(osp.join(self.root, self.image_paths[index]))
        target = self.name_to_label[self.labels[index][1]]

        if self.transform is not None:
            img = self.transform(img)

        if self.target_transform is not None:
            target = self.target_transform(target)

        return img, target
#'E:\pycharm\pycharmtest\yolo3-pytorch-master\VOCdevkit\VOC2007\Annotations'
#'E:\pycharm\pycharmtest\yolo3-pytorch-master\VOCdevkit\VOC2007\JPEGImages'
trainsdataset=MyDataset('E:\pycharm\pycharmtest\yolo3-pytorch-master\VOCdevkit\VOC2007')
print(trainsdataset)
#testdataset=MyDataset('E:\pycharm\pycharmtest\yolo3-pytorch-master\VOCdevkit\VOC2007\JPEGImages')
#trainloader = torch.utils.data.DataLoader(trainsdataset, batch_size=32, shuffle=False, num_workers=2)
#testloader = torch.utils.data.DataLoader(testdataset, batch_size=32, shuffle=False, num_workers=2)
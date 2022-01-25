from torchvision.datasets import VisionDataset
import mmcv
import os.path as osp
from PIL import Image


class SmokeDataset(VisionDataset):#torch.utils.data.DataLoader的前项处理函数   继承VisionDataset类
    def __init__(self, root, transform=None, target_transform=None):#定义函数输入为路径 transform和target_transform

        super(SmokeDataset, self).__init__(root, transform=transform,
                                           target_transform=target_transform)#获取VisionDataset的属性，并给VisionDataset类赋值

        paths = sorted(list(mmcv.scandir(self.root, recursive=True)))#mmcv.scandir可遍历提取到最底层文件信息，返回为路径列表

        self.image_paths = []
        self.labels = []
        labels = []
        for path in paths:#遍历文件路径列表
            if path.endswith('.json') and 'labels' in path:#判断满足文件结尾为.json and 在labels文件夹下
                label = mmcv.load(osp.join(self.root, path))['relationTagInfo'][0]['value']#mmcv.loadj读取json文件标注信息 返回为字典
                self.labels.append((path, label))
                labels.append(label)
            elif path.endswith('.jpg') and 'images' in path:
                self.image_paths.append(path)

        assert len(self.image_paths) == len(self.labels)  #判断图片数量和标签数量是否一直
        for image_path, (label_path, _) in zip(self.image_paths, self.labels):
            assert osp.splitext(osp.basename(image_path))[0] == osp.splitext(osp.basename(label_path))[0]#osp.basename提取文件名
                                                                                                # osp.splitext将文件id和后缀分开

        unique_labels = set(labels)#取出label元组
        self.name_to_label = {name: label for label, name in enumerate(unique_labels)}#将标签号和标签含义对应

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



#1424554766054490118.json
#/data/lijiashun/data/smoke/test/加油站_抽烟多分类v2_测试集_正向样本v1.2/labels
#
'''
import mmcv
alabels=[]
labels=[]
path='1424554766054490118.json'
label = mmcv.load(osp.join('/data/lijiashun/data/smoke/test/加油站_抽烟多分类v2_测试集_正向样本v1.2/labels', path))['relationTagInfo'][0]['value']#mmcv.loadj读取json文件标注信息 返回为字典
alabels.append((path, label))
labels.append(label)
print(label)
print(alabels)
print(labels)
'''
#out:正对确定抽烟
#[('1424554766054490118.json', '正对确定抽烟')]
#['正对确定抽烟']
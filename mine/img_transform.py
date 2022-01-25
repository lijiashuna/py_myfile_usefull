from PIL import Image, ImageDraw
import cv2
import os
import numpy as np
import random as r
from torchvision.transforms import transforms

root_path='H:/lijiashun/analysis/cuojian_ori'
for filename in os.listdir(root_path):

    imgpath = root_path + '/' + filename

    img = Image.open(imgpath)
    size = img.size
    img = transforms.RandomResizedCrop((int(size[1]*0.9),int(size[0]*0.9)))(img)
    img.save('H:/lijiashun/analysis/tmp/loujian1' + '/' + filename)

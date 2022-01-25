import cv2
from PIL import Image, ImageDraw
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
import numpy as np



def rawimage_box(x,img):
    for line in x:
        #print(line[0])
        x_top = int(line[0])

        y_top = int(line[1])

        x_bot = int(line[2])

        y_bot = int(line[3])

        line[4] = round(line[4],2)
        draw = ImageDraw.Draw(img)
        draw.rectangle([int(x_top), int(y_top), int(x_bot),int( y_bot)],  width = 5)
        draw.text((x_top,y_top),str(line[4]), fill=(255, 0, 0))
    img.save('H:/lijiashun/anaysis/loujian/' + '' )

imgpath = 'E:/pycharm/pycharmtest/mine/0.jpg'
img = Image.open(imgpath)
#img = cv2.imread(imgpath)
input=[[53, 11, 281, 479, 0.9792869091033936]]
#input.tolist()
rawimage_box(input,img)


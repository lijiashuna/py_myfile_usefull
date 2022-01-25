import requests
import base64
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
    img.save('H:/lijiashun/anaysis/cuo_ori/' + '' )


image_path = '0.jpg'

file = open(image_path, 'rb')
data = file.read()
encode_data = base64.b64encode(data)

post_data = {
    'model': 'ai-auto-common-detection-person'
}

ip = '172.31.3.250'
res = requests.post(url="http://{}:5000/init_model".format(ip), data=post_data)
print(res.text)

post_data = {
    'image': encode_data
}

res = requests.post(url="http://{}:5000/inference".format(ip), data=post_data)
print(res.text)

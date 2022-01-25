import cv2
import numpy as np
from PIL import Image, ImageDraw
from PIL import ImageFile
import os



img_root=''
for filename in os.listdir(img_root):
    img=cv2.imread(img_root + '/' + filename ,cv2.IMREAD_UNCHANGED)
    sobelx=cv2.Sobel(img,cv2.CV_64F,dx=1,dy=0)
    sobelx=cv2.convertScaleAbs(sobelx)
    sobely=cv2.Sobel(img,cv2.CV_64F,dx=0,dy=1)
    sobely=cv2.convertScaleAbs(sobely)
    result=cv2.addWeighted(sobelx,0.5,sobely,0.5,0)
    cv2.imshow("priginal",img)
    cv2.imshow("sobelx",sobelx)
    cv2.imshow("sobely",sobely)
    cv2.imshow("result",result)
    cv2.waitKey()
    cv2.destroyAllWindows()
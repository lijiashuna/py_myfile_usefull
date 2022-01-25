import os.path as osp
import os
import shutil

iou = 0
loujian = 0
loujian_list = []
wucha = 0
wucha_list = []
cuojian = 0
cuojian_list = []


def compute_IOU(rec1, rec2):
    """
    计算两个矩形框的交并比。
    :param rec1: (x0,y0,x1,y1)      (x0,y0)代表矩形左上的顶点，（x1,y1）代表矩形右下的顶点。下同。
    :param rec2: (x0,y0,x1,y1)
    :return: 交并比IOU.
    """
    left_column_max = max(rec1[0], rec2[0])
    right_column_min = min(rec1[2], rec2[2])
    up_row_max = max(rec1[1], rec2[1])
    down_row_min = min(rec1[3], rec2[3])
    # 两矩形无相交区域的情况
    if left_column_max >= right_column_min or down_row_min <= up_row_max:
        return 0
    # 两矩形有相交区域的情况
    else:
        S1 = (rec1[2] - rec1[0]) * (rec1[3] - rec1[1])
        S2 = (rec2[2] - rec2[0]) * (rec2[3] - rec2[1])
        S_cross = (down_row_min - up_row_max) * (right_column_min - left_column_max)
        return S_cross / (S1 + S2 - S_cross)


def readTxt(filePath, filePath1, target):
    result, result1 = [], []
    global loujian
    global loujian_list
    global cuojian
    global cuojian_list
    global wucha
    global wucha_list
    global iou
    with open(filePath, 'r') as f:
        for line in f:
            num = list(line.split(' '))
            result.append(num)
    with open(filePath1, 'r') as f1:
        for line in f1:
            num1 = list(line.split(' '))
            result1.append(num1)
    if len(result) != len(result1):
        if len(result) > len(result1):
            loujian += 1
            lj.write(osp.basename(filePath) + '\n')
            imagename = osp.basename(filePath).replace('.txt', '.jpg')
            src = image_root_or + "/" + imagename
            wc_savedir = savedir + '/' + 'lj_or' + '/' + imagename
            shutil.copyfile(src, wc_savedir)
            src1 = image_root_back + "/" + imagename
            wc_savedir1 = savedir + '/' + 'lj_back' + '/' + imagename
            shutil.copyfile(src1, wc_savedir1)
            # loujian_list.append(osp.basename(filePath))
        else:
            cuojian += 1
            cj.write(osp.basename(filePath) + '\n')
            imagename = osp.basename(filePath).replace('.txt', '.jpg')
            src = image_root_or + "/" + imagename
            wc_savedir = savedir + '/' + 'cj_or' + '/' + imagename
            shutil.copyfile(src, wc_savedir)
            src1 = image_root_back + "/" + imagename
            wc_savedir1 = savedir + '/' + 'cj_back' + '/' + imagename
            shutil.copyfile(src1, wc_savedir1)
            # cuojian_list.append(osp.basename(filePath))
    else:
        for item, item1 in zip(result, result1):
            '''sum, sum1 = 0, 0
            for index in range(len(item)):
                #print(item,index,item[index])
                sum+=float(item[index])
                sum1+=float(item1[index])'''
            iou = compute_IOU(item[1:], item1[1:])
            if iou <= target:
                print(iou)
                wucha += 1

                wc.write(str(iou) + '    ' + osp.basename(filePath) + '\n')
                imagename = osp.basename(filePath).replace('.txt', '.jpg')
                src = image_root_or + "/" + imagename
                wc_savedir = savedir + '/' + 'wc_or' + '/' + imagename
                shutil.copyfile(src, wc_savedir)
                src1 = image_root_back + "/" + imagename
                wc_savedir1 = savedir + '/' + 'wc_back' + '/' + imagename
                shutil.copyfile(src1, wc_savedir1)


if __name__ == '__main__':
    txt_root = 'E:/pycharm/pycharmtest/data/train/label'
    txt_root1 = 'E:/pycharm/pycharmtest/data/test/label'
    image_root_or = ''
    image_root_back = ''
    savedir = ''
    file = os.listdir(txt_root)
    file1 = os.listdir(txt_root1)
    num = len(file)
    num1 = len(file1)
    assert num == num1
    with open('wucha.txt', 'w', encoding='utf-8') as wc:
        with open('cuojian.txt', 'w', encoding='utf-8') as cj:
            with open('loujian.txt', 'w', encoding='utf-8') as lj:
                for i in range(num):
                    filePath = txt_root + '/' + file[i]
                    filePath1 = txt_root1 + '/' + file1[i]
                    readTxt(filePath, filePath1, 0.80)
    print("漏检：%d 错检：%d 误差过大：%d" % (loujian, cuojian, wucha))

import json
import os
from glob import glob

dir_json = r"F:/com_file/oxface/unavailable/solo/"  # json文件的目录

jsons = glob(dir_json + "*.json", recursive=False)  # 搜寻该目录下所有后缀名为.json的文件路径，改为**/*.json recursive=True为所有子目录的
all_files = glob(dir_json + "*.*", recursive=False)

images = list(set(all_files).difference(set(jsons)))  # all_files中有而jsons中没有的,就是图片

with open(dir_json + 'points_data.txt', "w") as txt:
    for file in jsons:
        with open(file, 'r') as load_f:
            load_dict = json.load(load_f)
            # print("load_dict:", load_dict)
            label = load_dict["shapes"][0]["label"]  # 读取json中的标签信息
            points = load_dict["shapes"][0]["points"]  # 读取json中的点的信息
            points = [int(j) for i in points for j in i]  # 所有的点化为整数
            for i in images:
                if file.split(".")[0] == i.split(".")[0]:
                    txt.writelines("{0},{1},{2}\n".format(i, " ".join(str(i) for i in points), label))
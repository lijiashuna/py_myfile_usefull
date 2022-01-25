import os
import shutil

i = 0
for filename in os.listdir('H:/lijiashun/analysis/images'):
    if i < 1000:
        shutil.copy('H:/chongtai/通用模型/行人/ai-auto-test-行人检测/labels/' + filename.replace('.jpg','.xml'), 'H:/lijiashun/analysis/labels/' + filename.replace('.jpg','.xml'))
        i += 1

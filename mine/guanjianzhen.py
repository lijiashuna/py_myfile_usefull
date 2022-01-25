import os
i=1
root='H:\lijiashun\9.10行人'
for filename in os.listdir(root):
    #newname = "{:05d}".format(i) + ".jpg"
    #os.chdir('H:/lijiashun/2021819')
    command = "ffmpeg -i {} -vf select='eq(pict_type\,I)' -vsync 2  {}/%5d{}".format(root+'/'+filename, 'H:/lijiashun/upload_0910', '_908_'+filename+'.jpg')
    os.system(command)
    i+=1
print(i)
#-f image2 {}11111111
import os
i = 1
for filename in os.listdir('H:\测试集\人脸检测\copy'):
    newname = 'copy'+"{:05d}".format(i) + ".jpg"
    os.chdir('H:\测试集\人脸检测\copy')
    os.rename(filename,newname)
    i += 1
    #'ox_face_'+
#i = 1
#while i < 118:
    #j = 1
    #for filename in os.listdir('F:/com_file/oxface/test/recognition/'+"{:05d}".format(i)):
        #newname = "{:05d}".format(i) +'_' +"{:04d}".format(j)+".jpg"
        #os.chdir('F:/com_file/oxface/test/recognition/'+"{:05d}".format(i))
        #os.rename(filename,newname)
        #j+=1
    #i += 1
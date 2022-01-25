import torch
import torch.nn as nn
import torch.nn.functional as F
from torchsummary import summary


# class Mynet(nn.Module):
#     def __init__(self):
#         super(Mynet, self).__init__()
#         self.conv1 = nn.Conv2d(3, 32, 3, 1, 1)
#         self.conv2 = nn.Conv2d(3, 32, 3, 1, 1)
#
#         self.dense1 = nn.Linear(32 * 3 * 3, 128)
#         self.dense2 = nn.Linear(128, 10)
#
#     def forward(self, x):
#         x = self.conv1(x)
#         x = F.relu(x)
#         x = F.max_pool2d(x)
#         x = self.conv2(x)
#         x = F.relu(x)
#         x = F.max_pool2d(x)
#         x = self.dense1(x)
#         x = self.dense2(x)
#
#         return x
#
#
# model = Mynet()
# print(model)
# #summary(model.cuda(),input_size=[(3, 32, 32)],)
class Person(object):
    def __init__(self, name, age):
        self.name = "zhansgan"
        self.__age = 18

    @property
    def age(self):
        return self.__age

    def set_age(self, age):  # 定义函数来给self.__age赋值
        if age < 18:
            print('年龄必须大于18岁')
            return
        self.__age = age
        return self.__age


xm = Person(20)


#
# print(xm.age)
# print('----------')
# xm.set_age(10)
# print(xm.age)
# print('----------')
# xm.set_age(20)


class Rectangle(object):

    def __init__(self):
        self.width = 10

        self.height = 20


r = Rectangle()

print(r.width, r.height)

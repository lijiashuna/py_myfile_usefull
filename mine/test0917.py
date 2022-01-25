"""
https://leetcode-cn.com/problems/unique-paths/%20/
给定m行n列的网格，有一个机器人从网格[0,0]处出发，且只能往右或往下走，有多少条路径可以走到右下角？
1、状态：
1.1 最后一步：[m-1,n-1]
1.2 子问题：走到最后状态[m-1,n-1]的前一步是[m-2,n-1]或者[m-1,n-2]
设有X步从左上角走到[m-2,n-1]，有Y步从左上角走到[m-1,n-2]，那么从左上角走到右下角的方式有X+Y种
2、动态规划组成二：转移方程：
f[i,j]=f[i-1,j]+f[i,j-1]
3、初始条件和边界情况：
f[0,0]=1  #机器人只要一种方式进入左上角
边界情况：i=0 或者 j=0时，f[i,j]只要一种方式可以过来
4、计算顺序：从上到下，从左到右
results=[[1]*n]*m遇到bug，
原因是list的浅拷贝问题
list * n—>n shallow copies of list concatenated
n个list的浅拷贝的连接
修改其中的任何一个元素会改变整个列表
改写为循环赋值即可[([0]*n) for i in range(n)]
"""
import torch.utils.data.dataset
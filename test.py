# -*- coding: utf-8 -*-
# @Time    : 2020/8/6 上午9:28
# @Author  : Xie
# @File    : test.py
# @Discription :



from itertools import islice
a_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# 每隔2次打印
for i in islice(a_list, 0, None):
    print (i)
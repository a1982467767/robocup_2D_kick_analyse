#!/usr/bin env python
# -*-encoding: utf-8 -*-
# author: qian jipeng

import os
import sys
import shutil
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def walking_tree(path):

	file_list = []
	for root, subFolders, files in os.walk(path): #获取根path下的子文件夹，文件
		for file in files:
			if file[len(file) - 4:] == '.txt' :
				file_list.append(os.path.join(root, file))
			#file_list.append(file)
                  #将rcg文件和rcl文件名称放在file_list中
	return file_list

def read_file(path):
	"""Reads the content of the specified file"""

	file = open(path, "r")
	content = file.read()
	file.close()
	content = content.split("\n")
	return content



# 第一步 把 kick_dist and kick_angle and angle_count 数据集成在一个文件下,用于下一步画图
filepaths = ["T_avgkickdataByDist_u.txt","T_avgkickdataByAngle_u.txt","T_avgKickAngleCount_u.txt"]
#filepaths = ["T_avgkickdataByDist_u.txt","T_avgKickAngleCount_u.txt"]
result = 'result'

#对于rcg、rcl原文本的操作
if os.path.exists( result ):
	shutil.rmtree( result )#删除此目录中所有的数据，包括此目录

if not os.path.exists( result ):  #创建根目录
	os.makedirs( result )

for filepath in filepaths:
	f = read_file( filepath )
	pre_name = f[0].split('\t')[0].strip()	
	for line in f:
		line = line.split('\t')
		#print (line)
		if line[0] == '':
			continue
		line[0] = line[0].strip()
		line_name = line[0]
		if pre_name == line_name: #上一个name与当前name相同
			### 把 三种数据写进相应的文件中
			file = open(result + '/' + line_name + '.txt', 'a')
			file.write( "\t".join(line) + '\n')
		else:
			pre_name = line_name #保留上一个name
			file = open(result + '/' + line_name + '.txt', 'a')
			file.write( "\t".join(line) + '\n')


#第二步 通过循环将所有球队所有区域的子图画出
# 对上一步生成的各个球队的txt文件进行读取，并按照分区画图


# python3 draw_mul.py $team $area $team
file_list = walking_tree( result )
for file_ in file_list:
	for area in range[8]:
		

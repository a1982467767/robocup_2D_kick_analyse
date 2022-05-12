#!/usr/bin env python
# -*-encoding: utf-8 -*-
# author: qian jipeng

import os
import sys
import shutil
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''
def walking_tree(path):

	file_list = []
	for root, subFolders, files in os.walk(path): #获取根path下的子文件夹，文件
		for file in files:
			if file[len(file) - 4:] == '.txt' :
				file_list.append(os.path.join(root, file))
			#file_list.append(file)
                  #将rcg文件和rcl文件名称放在file_list中
	return file_list
'''

def read_file(path):
	"""Reads the content of the specified file"""

	file = open(path, "r")
	content = file.read()
	file.close()
	content = content.split("\n")
	return content



# 第一步 把 kick_dist and kick_angle and angle_count 数据集成在一个文件下,用于下一步画图
filepaths = ["./T_avgkickdataByDist_u.txt","./T_avgkickdataByAngle_u.txt","./T_avgKickAngleCount_u.txt"]
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

'''
#第二步 通过循环将所有球队所有区域的子图画出
# 对上一步生成的各个球队的txt文件进行读取，并按照分区画图
def plot_sub( file_, area):
	f = read_file(file_)
	# 获取文件的每一行
	count = 0

	fig = plt.figure(1, figsize = (25,10))
	# 遍历每一行
	for line in f:
		angle_count = []  # 用来存对应的line
		by_angle = []
		by_dist = []
		line = line.split('\t')
		if line[0] == '':
			continue
		#print (line)
		count += 1  # count 行数
		if int(line[-1]) == area:  # 3行数据
			times = 0		#用来计数，达到3就画图显示一下title
			#lines.append(line)
			# 新建一张画布,指定长宽比

			if count == (1 + area):
		
				times += 1
				by_dist.append(line[0] + line[-1])  # 队名处理加上分区
				for i in range(1,9):
					by_dist.append(float(format(float(line[i]) , '.2f')))

				# print(new_by_dist)			# ['CYRUS0', 0.0, 0.1, 0.07, 0.07, 0.13, 0.17, 0.18, 0.28]

				df3 = pd.DataFrame(by_dist[1:], index=['0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0'])
				del by_dist
				# print(df3)

				ax3 = fig.add_subplot(311)

				data3 = np.array(df3.T)		# 转置
				#print(data3)

				X3 = ['0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0']

				Sum3 = 0
				#print(data3.shape[0])
				for i in range(data3.shape[1]):  # lie shu
		
					Sum3 += data3[0][i]
					# print(Sum3)

					# print(data3[:,0])		# [0.   0.1  0.07 0.07 0.13 0.17 0.18 0.28]

					ax3.barh(' ', data3[0][i], height= 0.8, left=Sum3 - data3[0][i], alpha= 0.5)  # left	 参数来控制叠加
					plt.yticks([-0.6,0.6])
					plt.xticks([-0,1.0])
					#plt.legend(loc='upper left', fontsize= 6)
					plt.text(-0.12,-0.2,' Dist',va= 'bottom', fontsize=50)
					plt.text(0.3,0.6,'1:0.4  2:0.5  3:0.6  4:0.7  5:0.8  6:0.9  7:1.0', va= 'top', fontsize=30)
			
					# 打上数值
					if data3[0][i] > 0:	
				
						# plt.text(x,y,s,ha,va...)		x,y 是位置坐标
						plt.text(Sum3 - (data3[0][i] / 2.0),-0.2,'%.1f'%((data3[0][i])),ha='center', va= 'bottom', fontsize=50)
				

			###################################################################################### 画 kick_by_angle

			if count == (9 + area):
		
				times += 1
		
				tmp1 = line[0] + line[-1].strip()

				by_angle = [tmp1,float(line[1]),float(line[2]),float(line[3]),float(line[4]),float(line[5]),float(line[6]),\
					    float(line[7]),float(line[8]),float(line[9]),float(line[10]),float(line[11]),float(line[12])]
				# print(new_by_angle)		# ['CYRUS0', '0.47', '0.20', '0.11', '0.05', '0.04', '0.03', '0.02', '0.03', '0.01', '0.02', '0.02', '0.01']

				df2 = pd.DataFrame(by_angle[1:], index=['dir15', 'dir30', 'dir45', 'dir60', 'dir75', 'dir90', 'dir105', 'dir120',
										  'dir135', 'dir150', 'dir165', 'dir180'])
				# print(df2)

				data2 = np.array(df2.T)
				# print(data2)

				ax2 = fig.add_subplot(312)

				X2 = ['dir15', 'dir30', 'dir45', 'dir60', 'dir75', 'dir90', 'dir105', 'dir120', 'dir135', 'dir150',
					  'dir165', 'dir180']

				Sum2 = 0
				for i in range(data2.shape[1]):  # hang shu

					Sum2 += data2[0][i]
					# print(Sum2)

					ax2.barh(' ', data2[0][i], height= 0.8, left=Sum2 - data2[0][i], alpha= 0.5)  # left	 参数来控制叠加
					plt.yticks([-0.6,0.6])
					plt.xticks([-0,1.0])
					#plt.legend(loc='upper left', fontsize= 6)
					plt.text(-0.14,-0.2,'Angle',va= 'bottom', fontsize=50)
					plt.text(0.2,0.6,'1:dir15 2:dir30 3:dir45 4:dir60 ------ 11:dir165 12:dir180', va= 'top', fontsize=30)
					# 打上数值
					if data2[0][i] > 0.05:	
				
						# plt.text(x,y,s,ha,va...)		x,y 是位置坐标
						plt.text(Sum2 - (data2[0][i] / 2.0),-0.2,'%.1f'%((data2[0][i])),ha='center', va= 'bottom', fontsize=50)


			######################################################################################  画 angle_count --- the start

			if count == (17 + area):
		
				angle_count.append(line[0] + line[-1])  # 队名处理加上分区
				angle_count.append(line[2])
				angle_count.append(line[3])
				angle_count.append(line[4])

				df1 = pd.DataFrame(angle_count[1:], index=['pass', 'dribble', 'hold'])

				df1.iat[0, 0] = float(format(float(df1.iat[0, 0]) , '.2f'))  # 小数点后两位
				df1.iat[1, 0] = float(format(float(df1.iat[1, 0]) , '.2f'))
				df1.iat[2, 0] = float(format(float(df1.iat[2, 0]) , '.2f'))


				ax1 = fig.add_subplot(313)

				data1 = np.array(df1.T)

				X1 = ['pass', 'dribble', 'hold']

				Sum1 = 0
				for i in range(data1.shape[1]):  # hang shu

					Sum1 += data1[0][i]
					# print(Sum2)

					ax1.barh(' ', data1[0][i], height= 0.8, left=Sum1 - data1[0][i], alpha= 0.5)  # left	 参数来控制叠加
					plt.yticks([-0.6,0.6])
					plt.xticks([-0,1.0])
					#plt.legend(loc='upper left', fontsize= 6)
					plt.text(-0.14,-0.2,'Action',va= 'bottom', fontsize=50)
					plt.text(0.4,0.6,'1:pass 2:dribble 3:hold', va= 'top', fontsize=30)
					# 打上数值
					if data1[0][i] > 0:	
						# plt.text(x,y,s,ha,va...)		x,y 是位置坐标
						plt.text(Sum1 - (data1[0][i] / 2.0),-0.2,'%.1f'%((data1[0][i])*100),ha='center', va= 'bottom', fontsize=50)
	
	

	if not os.path.exists( file_[:-4] ):  #创建根目录
		os.makedirs( file_[:-4] )
	file_name = file_[:-4] + "/" + file_[:-4].strip('/')[-1] + str(area) + '.png'
	plt.savefig(file_name)
	plt.cla()


# python3 draw_mul.py $team $area $team
file_list = walking_tree( result )

for file_ in file_list:
	for area in range(8): #用两层循环替代脚本
		plot_sub( file_, area)

'''



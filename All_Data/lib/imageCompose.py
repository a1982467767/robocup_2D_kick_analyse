#!/usr/bin/env/ python3
# encoding: utf-8
# author: YuShan2d Qian Jipeng
# 将所有球队的各个分区的单个图片合成成一张图片，存入相应的文件夹下

import os
import sys
import PIL.Image as Image


current_dir = os.getcwd()
#print(current_dir)


team_list =  sys.argv[1][:-4]
#['HELIOS2011','HELIOS2012','HELIOS2013','HELIOS2014','HELIOS2015','HELIOS2016','HELIOS2017','HELIOS2018', 'Gliders2013','Gliders2014','Gliders2015','Gliders2016','CYRUS','CYRUS2014','CYRUS2018','HfutEngine2017','HfutEngine2018','MT2018SS','MT2018GS','MT2018SJB','Oxsy']




obj_path = os.path.join(current_dir,team_list) + "/"
files = os.listdir(obj_path)	# 8张图片
#print(files)		# 乱序

#files.sort(key= lambda x: int (x[-5]))
'''
if len(files) != 8:
	raise ValueError("球队文件夹下图片数量不对")
'''
i = team_list
team = i		# 队名
n_image_name = team + '.png'	

newfiles = [team+'0.png',team+'2.png',team+'4.png',team+'6.png',team+'1.png',team+'3.png',team+'3.png',team+'7.png',team+'0.png',team+'2.png',team+'4.png',team+'6.png']


to_image = Image.new('RGB',(1920,1080))
#to_image = Image.open(os.getcwd() + "/soccer.png").resize((1920*4,1080*3))

for y in range(1, 4): 	# 行数
	for x in range(1, 5): 		# 列数
		from_image = Image.open(obj_path + newfiles[4 * (y - 1) + x - 1]).resize((480,360))
		
		
			
		to_image.paste(from_image, ((x - 1) * 480, (y - 1) * 360)) 	# box 参数

to_image.save(obj_path + n_image_name)

print("{} composed ok!".format(i))

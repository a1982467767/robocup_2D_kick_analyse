#!/usr/bin/python
#-*-coding:utf-8-*
"""
Copyright (C) 2018 YuShan2D SunChen 
python extra.py  ../LOG/ max_extra_size
"""

import sys,time,shutil
import os,datetime,math
sys.path.append("lib")
import ext_kick_data as ekd
import kick_count as kc
import dist_count as dc
import angle_count as ac
if __name__ == "__main__":  #主程序入口
	file_path = "./logs"  #录像存放位置
	max_ext = 100000
	time_str = datetime.datetime.now().strftime('%g%m%d%H%M%S') #时间str
	#time_str = "181029204401"
	if len(sys.argv) > 1:
		file_path = sys.argv[1]
		mydir = os.path.abspath(file_path)
		time_str = mydir.split("/")[-1]
	if len(sys.argv) > 2:
		max_ext = int(sys.argv[2])

	if not os.path.exists("./result"):  #创建根目录
		os.makedirs("./result")

	save_path = "./result" + "/" + time_str
	if os.path.exists(save_path): 
		shutil.rmtree(save_path)
	os.makedirs(save_path)

	ekd.ext_data(time_str, file_path, save_path, max_ext)
	kc.kick_anl(time_str, save_path) #当数据提取成功后解析数据
	dc.kick_anl(time_str, save_path) #按距离解析数据
	ac.kick_anl(time_str, save_path) #按角度解析数据

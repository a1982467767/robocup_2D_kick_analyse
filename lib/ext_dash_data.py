#!/usr/bin/python
#-*-coding:utf-8-*
"""
Copyright (C) 2018 YuShan2D SunChen 
"""
import sys,time
import os,datetime,math
import file_manager as fm
import show_process as sp
import get_data as gd

def ext_data( file_path, max_ext):
	file_list = fm.walking_tree(file_path)
	process_bar = sp.ShowProcess(min(max_ext,len(file_list)), 'OK')
	for i in range(min(max_ext,len(file_list))):
		process_bar.show_process()  #刷新进度
		time.sleep(0.01)
		sroot = file_list[i][0][5:-4].split("/")[-1]
		print ("["+sroot)
		rcg = fm.read_file(file_list[i][0])
		rcl = fm.read_file(file_list[i][1])
		teams = fm.find_teams(rcg)
		gd.get_dash_data(rcl,teams)	

if __name__ == "__main__":  #主程序入口
	ext_data()




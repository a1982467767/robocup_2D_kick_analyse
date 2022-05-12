#!/usr/bin/python3
#-*-coding:utf-8-*
"""
Copyright (C) 2018 YuShan2D SunChen 
"""

import sys,time,shutil
import os,datetime,math
sys.path.append("lib")
import kick_count as kc
import dist_count as dc
import angle_count as ac
if __name__ == "__main__":  #主程序入口
	kc.kick_anl_all() #当数据提取成功后解析数据
	dc.kick_anl_all() #按距离解析数据
	ac.kick_anl_all() #按角度解析数据

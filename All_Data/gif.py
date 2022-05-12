#!/usr/bin/python3
# coding=utf-8
"""
Copyright (C) 2018 YuShan2D SunChen 
"""
import sys
import matplotlib.pyplot as plt
import imageio,os
TIME_GAP=3

FILE_PATH= sys.argv[1]

def create_gif(image_list, gif_name):  
	print(image_list)
	frames = []  
	for image_name in image_list:  
		frames.append(imageio.imread(image_name))  
 
	imageio.mimsave(gif_name, frames, 'GIF', duration = TIME_GAP)  
	return 
 

if __name__ == '__main__':
	pngFiles = os.listdir(FILE_PATH) 
	image_list = [os.path.join(FILE_PATH, f) for f in pngFiles]
	image_list = sorted(image_list)
	create_gif(image_list, FILE_PATH + FILE_PATH[:-1] + '.gif')

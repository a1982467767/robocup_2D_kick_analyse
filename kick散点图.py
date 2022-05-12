#!/usr/bin/python3
# coding=utf-8
"""
Copyright (C) 2018 YuShan2D SunChen 
"""
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import Series,DataFrame


filename = "MT_kick.txt"
if len(sys.argv) == 2:
	filename = sys.argv[1]

data = np.loadtxt(filename)
plt.scatter(data[:,0],data[:,1])
plt.show()

plt.title("Angle")
fsize = 10
if(len(tips)<10):
	fsize = len(tips)
if(len(tips)<7):
	fsize = 7
plt.legend(loc='upper right',fontsize=fsize) #线条标签
plt.savefig("{}.jpg".format(filename[:-4]+"_barh"))
plt.show()

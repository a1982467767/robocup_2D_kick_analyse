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


filename = "angle-YuShan.txt"
if len(sys.argv) == 2:
	filename = sys.argv[1]
tips = pd.read_table(filename)

print (tips)

rows= [row for row in tips]
print (rows)

lows = [tips.get_value(x,'team').lstrip() for x in range(len(tips)) ]
print (lows)
party_counts = tips.ix[0:,1:13].values

party_counts = DataFrame(party_counts,index = lows, columns = pd.Index(rows[1:13],name = 'Data')) 

#然后进行归一化是各行和为1
df = party_counts.div(party_counts.sum(1).astype(float),axis = 0)
print( df)

df.plot(kind = 'barh',stacked = True,figsize=(12,len(tips)*0.5),rot=-5,colormap='Set3_r') #secondary_x=True绘制双y轴
#colormap认为可用参数：Set3_r、Pastel2、prism、rainbow、spring、PuBu_r、RdPu

my_x_ticks = np.arange(0, 1.01, 0.05) 
plt.xticks(my_x_ticks)
#kind 	可以是’line’(折线图), ‘bar’（柱状图）, ‘barh’（转置柱状图）, ‘kde’（连续型线图） ,stacked 是否叠加
plt.grid(b=True, which='major', axis='x') # formats the grid line style of our graphs
#team	dir15	dir30	dir45	dir60	dir75	dir90	dir105	dir120	dir135	dir150	dir165	dir180	goal	all
for i in range(0,len(lows)):
    plt.text(df.get_value(lows[i],'dir15')/2.0,i-0.30,'%.1f%s'% (df.get_value(lows[i],'dir15')*100,"%"), ha='center', va='bottom',color = 'r')
    plt.text(df.get_value(lows[i],'dir15')+df.get_value(lows[i],"dir30")/2.0,i-0.30,'%.1f%s'% (df.get_value(lows[i],'dir30')*100,"%"), color = 'b',ha='center', va='bottom')
    plt.text(df.get_value(lows[i],'dir15')+df.get_value(lows[i],"dir30")+df.get_value(lows[i],"dir45")/2.0,i-0.30,'%.1f%s'% (df.get_value(lows[i],'dir45')*100,"%"), ha='center', va='bottom',color = 'w')
    plt.text(df.get_value(lows[i],'dir15')+df.get_value(lows[i],"dir30")+df.get_value(lows[i],"dir45") + df.get_value(lows[i],"dir60")/2.0,i-0.30,'%.1f%s'% (df.get_value(lows[i],'dir60')*100,"%"), ha='center', va='bottom',color = 'k')
    #plt.text(df.get_value(lows[i],"dir45"),i,'%.0f'% df.get_value(lows[i],"dir45"), ha='center', va='bottom')

plt.title("Angle")
fsize = 10
if(len(tips)<10):
	fsize = len(tips)
if(len(tips)<7):
	fsize = 7
plt.legend(loc='upper right',fontsize=fsize) #线条标签
plt.savefig("{}.jpg".format(filename[:-4]+"_barh"))
plt.show()

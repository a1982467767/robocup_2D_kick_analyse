#!/usr/bin/python
#-*-coding:utf-8-*
"""
Copyright (C) 2018 YuShan2D SunChen 
"""
import sys
import matplotlib.pyplot as plt
import numpy as np 
import PIL.Image as Image

def init_field(teams,Team_name):
	fig = plt.figure(figsize=(25,15)) #图标长、宽
	# 画圆================================================================================begin
	# 1.圆半径
	r = 10.0
	# 2.圆心坐标
	a, b = (0., 0.)
	theta = np.arange(0, 2*np.pi, 0.01)
	x = a + r * np.cos(theta)
	y = b + r * np.sin(theta)
	axes = fig.add_subplot(111) 
	axes.plot(x, y,color = "g", linestyle = "-", linewidth = 3)
	#画圆=================================================================================end
	#球场建模================================================================================================begin
	#Draws field
	axes.plot([0, 0], [-34, 34], color = "g", linestyle = "-", linewidth = 3)
	axes.plot([-52.5, 52.5], [-34, -34], color = "g", linestyle = "-", linewidth = 3)
	axes.plot([-52.5, 52.5], [34, 34], color = "g", linestyle = "-", linewidth = 3)
	axes.plot([-52.5, -52.5], [-34, 34], color = "g", linestyle = "-", linewidth = 3)
	axes.plot([52.5, 52.5], [-34, 34], color = "g", linestyle = "-", linewidth = 3)
	#中文段落注释：color参数对应g-绿色，k-黑色，y-黄色，r-红色，linestyle对应的是线条模式，此处为破折线
	#Draws penalty area
	axes.plot([36, 52.5], [-20, -20], color = "g", linestyle = "-", linewidth = 3)
	axes.plot([36, 52.5], [20, 20], color = "g", linestyle = "-", linewidth = 3)
	axes.plot([36, 36], [-20, 20], color = "g", linestyle = "-", linewidth = 3)
	axes.plot([-36, -52.5], [-20, -20], color = "g", linestyle = "-", linewidth = 3)
	axes.plot([-36, -52.5], [20, 20], color = "g", linestyle = "-", linewidth = 3)
	axes.plot([-36, -36], [-20, 20], color = "g", linestyle = "-", linewidth = 3)
	axes.plot([47, 52.5], [-10, -10], color = "g", linestyle = "-", linewidth = 3)
	axes.plot([47, 52.5], [10, 10], color = "g", linestyle = "-", linewidth = 3)
	axes.plot([47, 47], [-10, 10], color = "g", linestyle = "-", linewidth = 3)
	axes.plot([-47, -52.5], [-10, -10], color = "g", linestyle = "-", linewidth = 3)
	axes.plot([-47, -52.5], [10, 10], color = "g", linestyle = "-", linewidth = 3)
	axes.plot([-47, -47], [-10, 10], color = "g", linestyle = "-", linewidth = 3)
	#Draw goal
	axes.plot([-53.5, -53.5], [-7, 7], color = "k", linestyle = "-", linewidth = 15)
	axes.plot([53, 53], [-7, 7], color = "k", linestyle = "-", linewidth = 15)

	#画虚线===============================================================================begin
	axes.plot([-72, 72], [-17, -17], color = "b", linestyle = "--", linewidth = 3)
	axes.plot([-72, 72], [17, 17], color = "b", linestyle = "--", linewidth = 3)
	axes.plot([36.0, 36.0], [-50, 50], color = "b", linestyle = "--", linewidth = 3)
	axes.plot([-1.0, -1.0], [-50, 50], color = "b", linestyle = "--", linewidth = 3)
	axes.plot([-36.0, -36.0], [-50, 50], color = "b", linestyle = "--", linewidth = 3)
	#画虚线===============================================================================end
	#设置坐标轴范围 
	axes.set_xlim((-70, 70)) 
	axes.set_ylim((-50, 50)) 
	#设置坐标轴名称 
	axes.set_xlabel('the distribution by x',fontsize=20) 
	axes.set_ylabel('the distribution by y',fontsize=20)
	 #设置坐标轴刻度 
	my_x_ticks = np.arange(-70, 70, 5) 
	my_y_ticks = np.arange(-50, 50, 2) 
	axes.set_xticks(my_x_ticks) 
	axes.set_yticks(my_y_ticks)
	#球场建模================================================================================================end
	axes.text(-58, 0, teams[0], color = "y", rotation = "vertical")
	axes.text(56, 0, teams[1], color = "r", rotation = "vertical")

	axes.text(-5, 52, Team_name.split('/')[0], color = "r",fontsize=30)

	#区域标签===============================================================================begin
	axes.text( -39, -27,"Area0:CrossBlock", color = "r",fontsize=20,rotation = "vertical")
	axes.text( -39, 40,"Area0:CrossBlock", color = "r",fontsize=20,rotation = "vertical")
	axes.text( -39, 3,"Area1:Danger", color = "r",fontsize=20,rotation = "vertical")
	axes.text( -4, -25,"Area2:DribbleBlock", color = "r",fontsize=20,rotation = "vertical")
	axes.text( -4, 41,"Area2:DribbleBlock", color = "r",fontsize=20,rotation = "vertical")
	axes.text( -4, 7,"Area3:DefMidField", color = "r",fontsize=20,rotation = "vertical")
	axes.text( 33, 41,"Area4:DribbleAttack", color = "r",fontsize=20,rotation = "vertical")
	axes.text( 33, -25,"Area4:DribbleAttack", color = "r",fontsize=20,rotation = "vertical")
	axes.text( 33, 7,"Area3:OffMidField", color = "r",fontsize=20,rotation = "vertical")
	axes.text( 67, 38,"Area6:Cross", color = "r",fontsize=20,rotation = "vertical")
	axes.text( 67, 9,"Area7:ShootChance", color = "r",fontsize=20,rotation = "vertical")
	axes.text( 67, -29,"Area6:Cross", color = "r",fontsize=20,rotation = "vertical")
	#区域标签===============================================================================end

	#plt.show()
	plt.savefig("soccer" + ".png")
	from_image = Image.open("soccer.png").resize((2120,1250))
	box = (160, 80, 2080, 1160)              ##确定拷贝区域大小
	region = from_image.crop(box)   
	region.save("soccer.png")
	img1 = Image.open( "soccer.png")
	img1 = img1.convert('RGBA')

	img2 = Image.open( Team_name + ".png")
	img2 = img2.convert('RGBA')
	img = Image.blend(img1, img2, 0.7)
	#img.show()
	img.save(Team_name + ".png")

Team_name = sys.argv[1][:-4]
Team_name = Team_name + "/" + Team_name
init_field(["left","right"],Team_name)








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

def ext_data(time_str, file_path, save_path, max_ext):
	result_path = os.path.abspath( save_path ) + "/" #结果存放在当前目录
	file_list = fm.walking_tree(file_path)
	result_file = result_path + "kickAngleCount.txt"
	if os.path.exists(result_file):
		os.remove(result_file)#删除此目录中所有的数据，包括此目录
	#获得总文件进度条
	process_bar = sp.ShowProcess(min(max_ext,len(file_list)), 'OK')
	
	for i in range(min(max_ext,len(file_list))):
		sroot = file_list[i][0][5:-4].split("/")[-1]
		process_bar.show_process()  #刷新进度
		time.sleep(0.01)
		print ("["+sroot)
		rcg = fm.read_file(file_list[i][0])
		rcl = fm.read_file(file_list[i][1])
		teams = fm.find_teams(rcg)
		if "null" == teams[0] or "null" == teams[1]:#跳过空文件
			continue
		if "notfound" == teams[0] or "notfound" == teams[1]:#跳过空文件
			continue
		goals = [0,0]
		
		goal_l = sroot.split(teams[0])[1].split("-")[0].split("_")
		goal_r = sroot.split(teams[1])[1].split("-")[0].split("_")

		try:	#对点球的处理 常规进球比分/点球比分
			int(goal_l[-2])>=0
			int(goal_r[-2])>=0
			goals[0] = goal_l[-2] + "/" + goal_l[-1]
			goals[1] = goal_r[-2] + "/" + goal_r[-1]
		except:
			goals[0] = goal_l[-1]
			goals[1] = goal_r[-1]
		#print (goals)
		'''
		file_w = open( result_path +"kickAngleCount.txt","a+")
		file_w.write( "%s\t%s\t%8s\t%8s\t%5s\t%5s\t%7s\t%6s\t%6s\t%6s\t%6s\t%6s\t%6s\t%6s\t\n" % \
					(sroot.split("-")[0],"team","kick","mulkick","0~90","90~180","180~270","270~360","forward","back","less0.5","0.5~0.8","high0.8","goal") )
		file_w.close()
		'''
			
		ball_data = fm.get_ball_data(rcg) #球属性数据
		kick_data = fm.get_kick_data(rcl, ball_data, teams)  #yuan kick数据
		del ball_data #后面不使用ball_data 销毁它
		if len(kick_data) <= 10:  #跳过过小的文件
			continue
		player_data = gd.get_player_data(rcg,teams)  #球员位置数据

		kick_player_data = gd.combine_data_with_kicker(kick_data,player_data)  #联合数据 所有kick
		del kick_data #后面不使用kick_data 销毁它
		del player_data #后面不使用player_data 销毁它
		angle_count(kick_player_data,teams,goals,result_file)

	print  ("数据已成功解析,写入:"+ result_file )

def angle_count(combine_data,teams,goals,result_file):
	all_relat_angle_r = [[0 for i in range(2)] for j in range(8)]
	all_relat_angle_l = [[0 for i in range(2)] for j in range(8)]
	dist_r = [[0 for i in range(2)] for j in range(8)]
	dist_l = [[0 for i in range(2)] for j in range(8)]
	kicks = [[0 for i in range(2)] for j in range(8)]
	passes = [[0 for i in range(2)] for j in range(8)]
	dribbles = [[0 for i in range(2)] for j in range(8)]
	mulkick = [[0 for i in range(2)] for j in range(8)]
	recivers = [[0 for i in range(2)] for j in range(8)]
	loses = [[0 for i in range(2)] for j in range(8)]
	#faults = [0,0]
	#offsides = [0,0]
	#角度处理模块1
	countless45 = [[0.0 for i in range(2)] for j in range(8)]
	count45_90 = [[0.0 for i in range(2)] for j in range(8)]
	count_forward = [[0.0 for i in range(2)] for j in range(8)]
	count_back = [[0.0 for i in range(2)] for j in range(8)]
	count90_135 = [[0.0 for i in range(2)] for j in range(8)]
	count135_180 = [[0.0 for i in range(2)] for j in range(8)]

	#角度处理模块2
	count15 = [[0.0 for i in range(2)] for j in range(8)]
	count30 = [[0.0 for i in range(2)] for j in range(8)]
	count45 = [[0.0 for i in range(2)] for j in range(8)]
	count60 = [[0.0 for i in range(2)] for j in range(8)]
	count75 = [[0.0 for i in range(2)] for j in range(8)]
	count90 = [[0.0 for i in range(2)] for j in range(8)]
	count105 = [[0.0 for i in range(2)] for j in range(8)]
	count120 = [[0.0 for i in range(2)] for j in range(8)]
	count135 = [[0.0 for i in range(2)] for j in range(8)]
	count150 = [[0.0 for i in range(2)] for j in range(8)]
	count165 = [[0.0 for i in range(2)] for j in range(8)]
	count180 = [[0.0 for i in range(2)] for j in range(8)]

	#距离处理模块1
	count1 = [[0.0 for i in range(2)] for j in range(8)]
	count2 = [[0.0 for i in range(2)] for j in range(8)]
	count3 = [[0.0 for i in range(2)] for j in range(8)]
	count4 = [[0.0 for i in range(2)] for j in range(8)]
	count5 = [[0.0 for i in range(2)] for j in range(8)]
	count6 = [[0.0 for i in range(2)] for j in range(8)]
	count7 = [[0.0 for i in range(2)] for j in range(8)]
	count8 = [[0.0 for i in range(2)] for j in range(8)]
	count9 = [[0.0 for i in range(2)] for j in range(8)]
	count10 = [[0.0 for i in range(2)] for j in range(8)]

	#距离处理模块2
	countless_5 = [[0.0 for i in range(2)] for j in range(8)]
	count5_8 = [[0.0 for i in range(2)] for j in range(8)]
	counthigh_8 = [[0.0 for i in range(2)] for j in range(8)]

	totol = [[0 for i in range(2)] for j in range(8)]


	for elt in combine_data:
		#此段是对所有类型的数据进行统计
		#按照球的位置对数据进行分区
		#x 方向-36，-1, 36 为临界，y方向17为临界	划分为8个区域编号为0-7
		area = 0
		#通过位置得到area
		'''
        	     -34+-------+---------------+----------------+------+
			|	|		|		 |	|
			| area0	|     area2	|      area4	 |area6	|
 		     -17+-------+---------------+----------------+------+
			|	|		|		 |	|
			|	|		|		 |	|
		       0+ area1	+     area3	+      area5	 +area7	+
			|	| 		|		 |	|
			|	|		|		 |	|
		      17+-------+---------------+----------------+------+
			|	|		|		 |	|
			| area0	|     area2	|      area4	 |area6	|
		      34+-------+---------------+----------------+------+
		      -52.5    -36 	       -1		 36    52.5
		'''
		if elt[3] > 36 :
			if elt[4] > 17 or elt[4] < -17:
				area = 0
			else :
				area = 1
		elif elt[3] > -1:
			if elt[4] > 17 or elt[4] < -17:
				area = 2
			else :
				area = 3
		elif elt[3] > -36 :
			if elt[4] > 17 or elt[4] < -17:
				area = 4
			else :
				area = 5
		else:
			if elt[4] > 17 or elt[4] < -17:
				area = 6
			else :
				area = 7
		if elt[1] == teams[1]: #球场位置逆置 ，球场方向
			if area % 2 == 1:
				area = 8 - area
			else:
				area = 6 - area
		#print elt ,area
		if elt[1] == teams[0]:
			kicks[area][0] += 1
			if elt[8] == 0: #types == 表示为pass
				passes[area][0] += 1	
			elif elt[8] == 1: #types == 1表示为drbble
				dribbles[area][0] += 1	
			elif elt[8] == 2: #types == 2表示为多步踢
				mulkick[area][0] += 1	
			elif elt[8] == 3: #types == 3表示为reciver
				recivers[area][0] += 1	
			elif elt[8] == 4: #types == 4表示为lose
				loses[area][0] += 1	
			#elif elt[8] == 7: #types == 7表示为fault之前的一次kick
			#	faults[area][0] += 1	
			#elif elt[8] == 8: #types == 8表示为offside
			#	offsides[area][0] += 1	
		else:
			kicks[area][1] += 1
			if elt[8] == 0: #types == 表示为pass
				passes[area][1] += 1	
			elif elt[8] == 1: #types == 1表示为drbble
				dribbles[area][1] += 1	
			elif elt[8] == 2: #types == 2表示为多步踢
				mulkick[area][1] += 1	
			elif elt[8] == 3: #types == 3表示为reciver
				recivers[area][1] += 1	
			elif elt[8] == 4: #types == 4表示为lose
				loses[area][1] += 1
			#elif elt[8] == 7: #types == 7表示为fault之前的一次kick
			#	faults[area][1] += 1	
			#elif elt[8] == 8: #types == 8表示为offside
			#	offsides[area][1] += 1	
		if elt[8] != 3: #and elt[8] != 2: #这里只针对reciver数据
			continue
			
		#begin左右队公共计算部分
		th_pos = [elt[3]-elt[5],elt[4]-elt[6]]  #获取相对点
		dist = math.sqrt(th_pos[0]*th_pos[0] + th_pos[1]*th_pos[1])  #获取相对位置
		th_angle = getAngle(th_pos[0],th_pos[1]) #获取角度
	
		relatAngle = th_angle - elt[7]  #获取球的方向与body的相对角度
		if relatAngle < 0 : #去除负值角度
			relatAngle += 360
		#if relatAngle > 180 : #将大于180的角度按x轴对称
		#	relatAngle = 360 - relatAngle
		#end
		#begin 数据写入部分	
		'''
		if elt[1] == teams[0]:		
			all_relat_angle_r.append(relatAngle)
		else:
			all_relat_angle_l.append(relatAngle)
		angle_analyzer(all_relat_angle_r,all_relat_angle_l,teams,result_path,goals,mulkick)# 数值计算与统计部分(角度)
		'''


		if elt[1] == teams[0]:
			elt_l = relatAngle
			#角度处理模块1
			if elt_l <= 90:
				countless45[area][0] += 1
				count_forward[area][0] += 1
			elif elt_l <= 180:
				count_back[area][0] += 1
				count45_90[area][0] += 1
			elif elt_l <= 270:
				count90_135[area][0] += 1
				count_back[area][0] += 1
			else: #in 135~180
				count135_180[area][0] += 1
				count_forward[area][0] += 1

			#角度处理模块2

			if elt_l <= 15 or elt_l >= 345:
				count15[area][0] += 1
			elif elt_l <= 30 or elt_l >= 330:
				count30[area][0] += 1
			elif elt_l <= 45 or elt_l >= 315:
				count45[area][0] += 1
			elif elt_l <= 60 or elt_l >= 300:
				count60[area][0] += 1
			elif elt_l <= 75 or elt_l >= 285:
				count75[area][0] += 1
			elif elt_l <= 90 or elt_l >= 270:
				count90[area][0] += 1
			elif elt_l <= 105 or elt_l >= 255:
				count105[area][0] += 1
			elif elt_l <= 120 or elt_l >= 240:
				count120[area][0] += 1
			elif elt_l <= 135 or elt_l >= 225:
				count135[area][0] += 1
			elif elt_l <= 150 or elt_l >= 210:
				count150[area][0] += 1
			elif elt_l <= 165 or elt_l >= 195:
				count165[area][0] += 1
			else: 
				count180[area][0] += 1
		else: #右队处理
			elt_r = relatAngle
			#角度处理模块1
			if elt_r <= 90:
				countless45[area][1] += 1
				count_forward[area][1] += 1
			elif elt_r <= 180:
				count45_90[area][1] += 1
				count_back[area][1] += 1
			elif elt_r <= 270:
				count90_135[area][1] += 1
				count_back[area][1] += 1
			else: #in 135~180
				count135_180[area][1] += 1
				count_forward[area][1] += 1
			#角度处理模块2
			if elt_r <= 15 or elt_r >= 345:
				count15[area][1] += 1
			elif elt_r <= 30 or elt_r >= 330:
				count30[area][1] += 1
			elif elt_r <= 45 or elt_r >= 315:
				count45[area][1] += 1
			elif elt_r <= 60 or elt_r >= 300:
				count60[area][1] += 1
			elif elt_r <= 75 or elt_r >= 285:
				count75[area][1] += 1
			elif elt_r <= 90 or elt_r >= 270:
				count90[area][1] += 1
			elif elt_r <= 105 or elt_r >= 255:
				count105[area][1] += 1
			elif elt_r <= 120 or elt_r >= 240:
				count120[area][1] += 1
			elif elt_r <= 135 or elt_r >= 225:
				count135[area][1] += 1
			elif elt_r <= 150 or elt_r >= 210:
				count150[area][1] += 1
			elif elt_r <= 165 or elt_r >= 195:
				count165[area][1] += 1
			else: 
				count180[area][1] += 1

		#距离处理
		if elt[1] == teams[0]:
		#距离处理模块1
			elt_dl = dist
			if elt_dl <= 0.1:
				count1[area][0] += 1
			elif elt_dl <= 0.2:
				count2[area][0] += 1
			elif elt_dl <= 0.3:
				count3[area][0] += 1
			elif elt_dl <= 0.4:
				count4[area][0] += 1
			elif elt_dl <= 0.5:
				count5[area][0] += 1
			elif elt_dl <= 0.6:
				count6[area][0] += 1
			elif elt_dl <= 0.7:
				count7[area][0] += 1
			elif elt_dl <= 0.8:
				count8[area][0] += 1
			elif elt_dl <= 0.9:
				count9[area][0] += 1
			else: 
				count10[area][0] += 1

			#距离处理模块2
			if elt_dl <= 0.5:
				countless_5[area][0] += 1
			elif elt_dl <= 0.8:
				count5_8[area][0] += 1
			else: 
				counthigh_8[area][0] += 1


			totol[area][0] += 1
		else: #右队处理
			elt_dr = dist
			if elt_dr <= 0.1:
				count1[area][1] += 1
			elif elt_dr <= 0.2:
				count2[area][1] += 1
			elif elt_dr <= 0.3:
				count3[area][1] += 1
			elif elt_dr <= 0.4:
				count4[area][1] += 1
			elif elt_dr <= 0.5:
				count5[area][1] += 1
			elif elt_dr <= 0.6:
				count6[area][1] += 1
			elif elt_dr <= 0.7:
				count7[area][1] += 1
			elif elt_dr <= 0.8:
				count8[area][1] += 1
			elif elt_dr <= 0.9:
				count9[area][1] += 1
			else: 
				count10[area][1] += 1

			#距离处理模块2
			if elt_dr <= 0.5:
				countless_5[area][1] += 1
			elif elt_dr <= 0.8:
				count5_8[area][1] += 1
			else: 
				counthigh_8[area][1] += 1

			totol[area][1] += 1
		
	
	#print totol
	#8区域数据输出处理
	#输出处理1

	for area in range(8):

		file_w = open( result_file[:-4]+ str(area) + ".txt","a+")
		#操作数据输出1——总体数据输出
		#team,总kick,pass,dribble,mulkick,lose,forward,back,less0.5,less0.8,high0.8.goals
		#print totol[area]
		if totol[area][0] == 0:
			file_w.write( "%s\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%s\n" % \
					( teams[0], 0, 0, 0, 0, 0, \
					 0.0, 0.0, \
					 0.0, 0.0, 0.0, goals[0]) )
		else:
			file_w.write( "%s\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%s\n" % \
					( teams[0], totol[area][0], passes[area][0], dribbles[area][0], mulkick[area][0], loses[area][0],\
					 count_forward[area][0]/totol[area][0] * 100, count_back[area][0]/totol[area][0] * 100, \
					 countless_5[area][0]/totol[area][0] * 100, count5_8[area][0]/totol[area][0] * 100, counthigh_8[area][0]/totol[area][0] * 100, goals[0]) )
		if totol[area][1] == 0:
			file_w.write( "%s\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%s\n" % \
				( teams[1], 0, 0, 0, 0, 0, \
					 0.0, 0.0, \
					 0.0, 0.0, 0.0, goals[1]) )
		else:
			file_w.write( "%s\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%s\n" % \
					( teams[1], totol[area][1], passes[area][1], dribbles[area][1], mulkick[area][1], loses[area][1], \
					 count_forward[area][1]/totol[area][1] * 100, count_back[area][1]/totol[area][1] * 100, \
					 countless_5[area][1]/totol[area][1] * 100, count5_8[area][1]/totol[area][1] * 100, counthigh_8[area][1]/totol[area][1] * 100, goals[1]) )
		file_w.close()

		#输出处理2
		file_w = open( result_file[:-18] + "kickdataByDist" + str(area) + ".txt","a+")
		#操作数据输出2——距离数据输出
		#比kicknum数据多一个
		#team,dist0.3,dist0.4,dist0.5,dist0.6,dist0.7,dist0.8,dist0.9,dist1.0,goals
		if totol[area][0] == 0:
			file_w.write( "%s\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%s\n" % \
					( teams[0], 0.0,\
					 0.0, 0.0, 0.0, \
	 				 0.0, 0.0, 0.0, \
					 0.0, goals[0]) )
		else:
			file_w.write( "%s\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%s\n" % \
					( teams[0], count3[area][0]/totol[area][0] * 100,\
					 count4[area][0]/totol[area][0] * 100, count5[area][0]/totol[area][0] * 100, count6[area][0]/totol[area][0] * 100, \
	 				 count7[area][0]/totol[area][0] * 100, count8[area][0]/totol[area][0] * 100, count9[area][0]/totol[area][0] * 100, \
					 count10[area][0]/totol[area][0] * 100, goals[0]) )
		if totol[area][1] == 0:
			file_w.write( "%s\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%s\n" % \
					( teams[1], 0.0,\
					 0.0, 0.0, 0.0, \
	 				 0.0, 0.0, 0.0, \
					 0.0, goals[1]) )
		else:
			file_w.write( "%s\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%s\n" % \
					( teams[1], count3[area][1]/totol[area][1] * 100,\
					 count4[area][1]/totol[area][1] * 100, count5[area][1]/totol[area][1] * 100, count6[area][1]/totol[area][1] * 100, \
	 				 count7[area][1]/totol[area][1] * 100, count8[area][1]/totol[area][1] * 100, count9[area][1]/totol[area][1] * 100, \
					 count10[area][1]/totol[area][1] * 100, goals[1]) )
		file_w.close()

		#输出处理3
		file_w = open( result_file[:-18]+"kickdataByAngle" + str(area) + ".txt","a+")
		#操作数据输出3
		#比kicknum数据多三个
		#team,less15,less30,less45,less60,less75,less90,less105,less120,less135,less150,less165,less180,goals
		if totol[area][0] == 0:
			file_w.write( "%s\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%s\n" % \
					( teams[0], 0.0, 0.0, 0.0,\
					 0.0, 0.0, 0.0, \
	 				 0.0, 0.0, 0.0, \
					 0.0,0.0, 0.0, goals[0]) )
		else:
			file_w.write( "%s\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%s\n" % \
					( teams[0], count15[area][0]/totol[area][0] * 100, count30[area][0]/totol[area][0] * 100, count45[area][0]/totol[area][0] * 100,\
					 count60[area][0]/totol[area][0] * 100, count75[area][0]/totol[area][0] * 100, count90[area][0]/totol[area][0] * 100, \
	 				 count105[area][0]/totol[area][0] * 100, count120[area][0]/totol[area][0] * 100, count135[area][0]/totol[area][0] * 100, \
					 count150[area][0]/totol[area][0] * 100,count165[area][0]/totol[area][0] * 100, count180[area][0]/totol[area][0] * 100, goals[0]) )
		if totol[area][1] == 0:
			file_w.write( "%s\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%s\n" % \
					( teams[1], 0.0, 0.0, 0.0,\
					 0.0, 0.0, 0.0, \
	 				 0.0, 0.0, 0.0, \
					 0.0,0.0, 0.0, goals[1]) )
		else:
			file_w.write( "%s\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%s\n" % \
					( teams[1], count15[area][1]/totol[area][1] * 100, count30[area][1]/totol[area][1] * 100, count45[area][1]/totol[area][1] * 100,\
					 count60[area][1]/totol[area][1] * 100, count75[area][1]/totol[area][1] * 100, count90[area][1]/totol[area][1] * 100, \
	 				 count105[area][1]/totol[area][1] * 100, count120[area][1]/totol[area][1] * 100, count135[area][1]/totol[area][1] * 100, \
					 count150[area][1]/totol[area][1] * 100,count165[area][1]/totol[area][1] * 100, count180[area][1]/totol[area][1] * 100, goals[1]) )

		file_w.close()


def getAngle(x, y):
	l = math.sqrt(x*x + y*y)
	angle = math.acos( x / l ) * 180 / math.pi
	if y < 0:
		angle = -angle
	return angle


if __name__ == "__main__":  #主程序入口
	time_str = datetime.datetime.now().strftime('%g%m%d%H%M%S') #时间str
	ext_data(time_str)




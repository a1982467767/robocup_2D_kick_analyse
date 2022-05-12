#!/usr/bin/python
#-*-coding:utf-8-*

import re #Regular Expression
import sys
import os
import math
"""
Module which reads log files and extracts data
Copyright (C) 2018 YuShan2D SunChen 
"""
#为了方便将列表转换成map可迭代列表，提供map的第一个参数
def donothing(x):
	return x

#
#获取进球
#
def get_goal_data(rcl,teams):
	"""Returns goal kick"""

	goal_kick_expr = "goal_[r|l]"
	cycle_expr = "^\d*" #
	tmp_cycle = list()
	goal_kick = list()
	all_goal = list()
	for elt in rcl:
		if "goal_" in elt and "goal_kick" not in elt:
			try:
				goal_k = re.search(goal_kick_expr, elt).group()
				goal_kick = goal_k.split("_")
				tmp_cycle = re.search(cycle_expr, elt).group()
				#print goal_kick
				if goal_kick[1] == "l":
					team = teams[0]
				else:
					team = teams[1]
				temp = [int(tmp_cycle),team]
				all_goal.append(temp)
			except:
				pass
	return all_goal #[cycle,team]

#
#获取进球周期
#
def get_goal_cycle(goal_data):
	goal_cycle=list()
	for elt in goal_data:
		goal_cycle.append(elt[0])
	return goal_cycle


#
#这里主要获取有效kick球之前的一个周期,并仿造kick数据(这里取多步kick的最前一步前一个周期)
#
def get_no_mutkick_data_pre(kick_data,teams):
	mutKick_totol = [0,0]
	no_mutkick_data_pre = list()
	pre = kick_data[0]
	#print (pre)
	for elt in kick_data:
		if pre[0] == elt[0]:
			continue
		if pre[0]+1 == elt[0] and pre[1] == elt[1] and pre[2] == elt[2]:
			if pre[1] == teams[0]:
				mutKick_totol[0] += 1
			else :
				mutKick_totol[1] += 1
		else:
			pre[0] -= 1
			no_mutkick_data_pre.append(pre)
		pre = elt
	#for i in no_mutkick_data_pre:
	#	print (i)
	return no_mutkick_data_pre,mutKick_totol

#这里主要获取有效kick,并仿造kick数据(这里取多步kick的最前一步)
def get_no_mutkick_data_pre1(kick_data,teams):
	mutKick_totol = [0,0]
	no_mutkick_data_pre = list()
	pre = kick_data[0]
	#print (pre)
	for elt in kick_data:
		if pre[0] == elt[0]:
			continue
		if pre[0]+1 == elt[0] and pre[1] == elt[1] and pre[2] == elt[2]:
			if pre[1] == teams[0]:
				mutKick_totol[0] += 1
			else :
				mutKick_totol[1] += 1
		else:
			no_mutkick_data_pre.append(pre)
		pre = elt
	#for i in no_mutkick_data_pre:
	#	print (i)
	return no_mutkick_data_pre,mutKick_totol

#这里主要获取有效kick,并仿造kick数据(这里取多步kick的最后一步)
def get_no_mutkick_data_last1(kick_data,teams):
	mutKick_totol = [0,0]
	no_mutkick_data_last = list()
	pre = kick_data[0]
	#print (pre)
	for elt in kick_data:
		if pre[0] == elt[0]:
			continue
		if pre[0]+1 == elt[0] and pre[1] == elt[1] and pre[2] == elt[2]:
			if pre[1] == teams[0]:
				mutKick_totol[0] += 1
			else :
				mutKick_totol[1] += 1
		else:
			no_mutkick_data_last.append(elt)
		pre = elt
	#for i in no_mutkick_data_last:
	#	print (i)
	return no_mutkick_data_last,mutKick_totol


#获取进球前五十个周期球的位置
def get50cyclebygoal(goal_cycle,ball_data):
	_50cycle=list()
	all_50cycle=list()
	len_goal_cycle = len(goal_cycle)
	len_ball_data = len(ball_data)
	for i in range(len_goal_cycle):
		count = 0
		for elt in range(len_ball_data):
			if ball_data[elt][0] > goal_cycle[i] - 50 and ball_data[elt][0] <= goal_cycle[i]:
				if count < 50:
					_50cycle.append(ball_data[elt])
					count+=1
				else:
					continue
			elif ball_data[elt][0] <= goal_cycle[i] - 50:
				continue
			else:
				break
		all_50cycle.append(_50cycle)
		_50cycle = []
	return all_50cycle


def all_50datatogather(all_50cycledata): 
	_all_50datatogather = list()
	for i in range(0,len(all_50cycledata)):
		for elt in all_50cycledata[i]:
			_all_50datatogather.append(elt)
	return _all_50datatogather


#获取场休息周期
def get_half_cycle(rcl,teams):
	"""Returns goal kick"""

	goal_kick_expr = "half_time"
	cycle_expr = "^\d*" #
	tmp_cycle = list()
	goal_kick = list()
	all_half = list()
	for elt in rcl:
		if "half_time" in elt:
			goal_k = re.search(goal_kick_expr, elt).group()
			goal_kick = goal_k.split("_")
			tmp_cycle = re.search(cycle_expr, elt).group()
			temp = int(tmp_cycle)
			all_half.append(temp)
	return all_half #[cycle]


#获取attentionto
def get_attentionto(rcl):
	"""Returns attention to date"""

	attention_expr = "atten[ 0-9a-z]*"
	reciver_expr = "Recv[ 0-9a-zA-Z-_]*"
	cycle_expr = "^\d*" #
	tmp_cycle = list()
	attention_to = list()
	attentionto_date = list()
	recv=list()
	att_num=-1
	teamname="deafult"
	for elt in rcl:
		if "attention" in elt:
			attention_to = re.search(attention_expr, elt).group()
			attention_to = attention_to.split(" ")#att off / att our unum
			recv = re.search(reciver_expr, elt).group()
			org = recv[len(recv)-1]
			recv = recv.split("_")
			recv[0] = recv[0][5:]
			#recv.append(org)
			tmp_cycle = re.search(cycle_expr, elt).group()
			if len(attention_to) == 3:
				att_num = attention_to[len(attention_to) - 1]
				#print att_num
			else :#len(attention_to) == 2:
				att_num = -1 #没有attention
			if len(recv) != 2:
				for i in range(1,len(recv)-1):
					recv[0] += "_" + recv[i]
					#print recv
					del(recv[i])
			temp = [int(tmp_cycle) + 1,recv[0],int(recv[1]),int(att_num)]
			#print temp
			attentionto_date.append(temp)
	#print attentionto_date
	return attentionto_date #[cycle,team,org_num,att_num]

	

def get_player_data(rcg,teams):
	"""Returns player data for each cycle"""
	player_data_expr = "\([r|l]*[ ][0-9]+\)[ ][0-9]+[ ][0-9x]*([ ][-]?[0-9]*(\.[0-9]*)?){6} "#10,11未匹配问题已经解决
	cycle_expr = "\(show [0-9]+" #周期匹配正则表达式
	player_data = list()

	for elt in rcg:
		player = list()
		if re.search(player_data_expr, elt) is not None:
			try:
				cycle = re.search(cycle_expr, elt).group()
				cycle = cycle.split(" ") 
				elt = elt.split("))")
			except:
				continue
		for elt1 in elt:
			if re.search(player_data_expr, elt1) is not None:
				try:
					tmp = re.search(player_data_expr, elt1).group()
					tmp = tmp.split(" ")		
					if tmp[0][-1:] == "r":
						player_team = teams[1]
					else:
						player_team = teams[0]
					player.append(int(cycle[1]))
					player.append(player_team)
					player.append(int(tmp[1][:-1]))
					player.append(float(tmp[4]))
					player.append(float(tmp[5]))
					player.append(float(tmp[6]))
					player.append(float(tmp[7]))
					player.append(float(tmp[8]))
					player.append(float(tmp[9]))
					player_data.append(player) #cycle,team,player_n,player_x,player_y,player_vx,player_vy,body,view
					player = list()
				except:
					pass
	#for i in player_data:
	#	print "%s #" % i #[[[left],[right]],[[]]...]
	return player_data #[cycle,team,player_n,player_x,player_y,player_vx,player_vy,body,view]


def combine_data(left_data,right_data): #左右数据合并,通过周期
	combine_da = list()
	temp = list()
	count = 0
	for elt in left_data:
		temp = []
		temp.append(elt)
		#print "%s #" % temp[0]
		while count < len(right_data):
			#print right_data[count]
			count = count + 1;
			if count+1 <= len(right_data)-1 and elt[0] == right_data[count][0] :			
				temp.append(right_data[count][1:])
			if count+1 <= len(right_data)-1 and count+1 <= len(right_data) and elt[0] < right_data[count+1][0]:
				break		
		combine_da.append(temp)
	#for i in combine_da:
	#	print "%s #" % i #[[[left],[right]],[[]]...]
	return combine_da  


#转门为计算kick在身体方向的函数
def combine_data_with_kicker(left_data,right_data): #左右数据合并,通过周期
	combine_da = list()
	temp = list()
	count = 0
	precycle = -1
	for elt in left_data:
		if elt[0] == precycle : #对多人同时踢球进行检测,如果有多个人同时踢球删除该周期的踢球数据
			del(combine_da[-1:])#删除最后一个数据
			continue
		temp = elt
		flag = 0	
		while count < len(right_data):
			count = count + 1;
			if count+1 <= len(right_data)-1 and elt[0] == right_data[count][0] and elt[1] == right_data[count][1] and elt[2] == right_data[count][2]:
				types = temp[7]
				del(temp[5:])
				flag = 1	#当有数据匹配成功设为1		
				temp.append(right_data[count][3])
				temp.append(right_data[count][4])
				temp.append(right_data[count][7])
				temp.append(types)
			if count+1 <= len(right_data)-1 and elt[0] < right_data[count+1][0]:
				break
		#当出现多个球员同时踢球时就会产生错误,故此处牺牲效率
		count = count - 1	
		if flag == 1:	
			combine_da.append(temp)
		precycle = elt[0] #保留上一个周期
	return combine_da #[cycle,team,num,ball_x, ball_y,kick_x,kick_y,body]


#专门为attentionto数据建立的合并函数
def combine_data_pro(left_data,right_data):
	combine_da = list()
	temp = list()
	count = 0
	for elt in left_data:
		temp = []
		temp.append(elt[:3])
		#print "%s #" % elt
		while count < len(right_data):
			#print right_data[count]
			count = count + 1;
			if count+1 <= len(right_data) and elt[0] + 1 == right_data[count][0] and elt[1] == right_data[count][1]:			
				temp.append(right_data[count][2:])
			if count+1 <= len(right_data)-1 and elt[0] + 1 < right_data[count+1][0]:
				break
		if len(temp) > 1:		
			combine_da.append(temp)
	for i in combine_da:
		#if i[0][0] == 64:
		print ( "%s #" % i) #[[5553, 'YuShan_NB', 9], [3, 11], [1, 5], [9, 10]] # kickcycle teamname unum [org_unum,target_unum](attention)
	return combine_da

#获取转身数据
def get_turn_data(rcl):
	"""Returns turn data for each cycle"""

	turn_data_expr = "Recv [a-zA-Z0-9]+([-_]*[0-9]*)*:" + \
	" \(turn ([ ]?[-]?[0-9][.]?)*"
	cycle_expr = "^[0-9]*" #
	turn_data = list()

	for elt in rcl:
		line = elt.split(" ")
		if len(line) > 2 and line[2] == "(turn":
			tmp_cycle = re.search(cycle_expr, elt).group()
			if re.search(turn_data_expr, elt): 
				tmp = re.search(turn_data_expr, elt).group()
				tmp = tmp.split(" ")
				agent = tmp[1].split("_")#球队和球员之间的信息进行拆分，获取球员信息
				if len(agent) != 2:
					while len(agent) > 2:
						agent[0] += "_" + agent[1]
						del agent[1]						
				turn_data.append([int(tmp_cycle)+1, agent[0], int(agent[1][:-1]),float(tmp[3])]) 

	return turn_data #[cycle,team,n,turn°]

#获取dash数据
def get_dash_data(rcl):
	"""Returns dash data for each cycle"""

	dash_data_expr = "Recv [a-zA-Z0-9]+([-_]*[0-9]*)*:" + \
	" \(dash ([ ]?[-]?[0-9][.]?)*"
	cycle_expr = "^[0-9]*" #
	dash_data = list()

	for elt in rcl:
		line = elt.split(" ")
		if len(line) > 2 and line[2] == "(dash":
			tmp_cycle = re.search(cycle_expr, elt).group()
			if re.search(dash_data_expr, elt): 
				tmp = re.search(dash_data_expr, elt).group()
				tmp = tmp.split(" ")
				agent = tmp[1].split("_")#球队和球员之间的信息进行拆分，获取球员信息
				if len(agent) != 2:
					while len(agent) > 2:
						agent[0] += "_" + agent[1]
						del agent[1]						
				dash_data.append([int(tmp_cycle)+1, agent[0], int(agent[1][:-1]),float(tmp[3])]) 
	
	#print dash_data
	return dash_data #[cycle,team,n,dash°]



def get_playon_data(rcl):
	"""Returns play_on cycle for each cycle"""

	cycle_expr = "^[0-9]*" 
	play_on_cycle = list()

	for elt in rcl:
		if "play_on" in elt:
			#print elt
			tmp_cycle = re.search(cycle_expr, elt).group()
			play_on_cycle.append(int(tmp_cycle) + 1)

	return play_on_cycle #[cycle,team,n,turn°]



#count turn before ball get 防守成功时turn 数据
def get_kick_player_turn(turn_data,kick_data):
	kick_player_turn = list()
	temp = list()
	pre_kick_data = kick_data[0]
	total_turn = 0
	i = 0
	is_swap = 0
	for kpt in kick_data[1:len(kick_data)]:
		cycle_during = kpt[0] - pre_kick_data[0]#保留上下两周期的周期间隔
		for i in range(0,len(turn_data)):
			if turn_data[i][0] >= pre_kick_data[0] and turn_data[i][0] < kpt[0]:
				if turn_data[i][1] == kpt[1] and turn_data[i][2] == kpt[2]:#从上个人拿到球，该队员共转身了多少次
					total_turn += 1	
				if kpt[1] != pre_kick_data[1]:
					is_swap = 1
				else:
					is_swap = 0					
			elif turn_data[i][0] == kpt[0]:
				break
			i = i + 1
		pre_kick_data = kpt           #保留前驱
		
		if is_swap == 1:              #保留交换球的数据在这个球转换周期内turn了多少次
			temp = kpt
			temp.append(total_turn)#将第七个参数设置为接球转身次数
			kick_player_turn.append(temp)
		total_turn = 0                #置零
	 	
	return kick_player_turn #[cycle,team,n,playerX,playerY,playerVX,playerVY,count_turn]

#count dash before ball get 防守成功时dash 数据
def get_kick_player_dash(dash_data,kick_data):
	kick_player_dash = list()
	temp = list()
	pre_kick_data = kick_data[0]
	total_dash = 0
	i = 0
	is_swap = 0
	for kpd in kick_data[1:len(kick_data)]:
		cycle_during = kpd[0] - pre_kick_data[0]#保留上下两周期的周期间隔
		for i in range(0,len(dash_data)):
			if dash_data[i][0] >= pre_kick_data[0] and dash_data[i][0] < kpd[0]:
				if dash_data[i][1] == kpd[1] and dash_data[i][2] == kpd[2]:#从上个人拿到球，该队员共dash了多少次
					total_dash += 1	
				if kpd[1] != pre_kick_data[1]:
					is_swap = 1
				else:
					is_swap = 0					
			elif dash_data[i][0] == kpd[0]:
				break
			i = i + 1
		pre_kick_data = kpd           #保留前驱
		
		if is_swap == 1:              #保留交换球的数据在这个球转换周期内dash了多少次
			temp = kpd
			temp.append(total_dash)#将第七个参数设置为接球转身次数
			kick_player_dash.append(temp)
		total_dash = 0                #置零
	
	print ( kick_player_dash )
	return kick_player_dash #[cycle,team,n,playerX,playerY,playerVX,playerVY,count_turn, count_dash]



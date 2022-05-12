#!/usr/bin/python
#-*-coding:utf-8-*

import re #Regular Expression
import sys
import os
import get_data as gd
import math

"""Module which reads log files and extracts data"""

def walking_tree(path):
	"""Walks the given path and returns a list of all logs' path"""

	file_list = []
	for root, subFolders, files in os.walk(path): #获取根path下的子文件夹，文件
		for file in files:
			if file[len(file) - 4:] == ".rcg" and file != "incomplete.rcg":
				rcl = os.path.join(root, file[: -3] + "rcl")#path目录下rcg 和rcl文件必须成对存在，否则会出错
				file_list.append([os.path.join(root, file), rcl])
                  #将rcg文件和rcl文件名称放在file_list中
	for elt in file_list: #对文件列表进行排序
		elt1 = elt
		elt = elt[0].split("-")
		del elt[0]
		#print(elt)
		if len(elt) > 3:
			i = 0
			x = 0
			while i < len(elt):
				if elt[i] == "vs":
					while x < i-1:
						elt[0] += "-" + elt[1]
						del elt[1]
						x += 1
					del elt[1]
					x = 0
					while x < len(elt) - 1 - i:
						elt[1] += "-" + elt[2]
						del elt[2]
						x += 1
					break
				i += 1
		if len(elt) == 3:
			del elt[1]
		elt1.insert(2, elt[0][:-2])
		elt1.insert(3, elt[1][:-6])
		#print (elt1)
												
	file_list = sorted(file_list, key=lambda x:(x[2],x[3]),reverse=True) #对主列表排序
	return file_list

def exists_walking_tree(path):

	file_list = []
	for root, subFolders, files in os.walk(path): #获取根path下的子文件夹，文件
		for file in subFolders:
			file_list.append(file)
                  #将rcg文件和rcl文件名称放在file_list中
	return file_list

def read_file(path):
	"""Reads the content of the specified file"""

	file = open(path, "r")
	content = file.read()
	file.close()
	content = content.split("\n")

	return content

def find_teams(rcg):
	"""Determines the name of both teams"""

	team_expr = "^\(team[ ][1]*[ ][a-zA-Z0-9]*([-]*[_]*[a-zA-Z0-9]*)*" + \
	"[ ][a-zA-Z0-9]*([-]*[_]*[a-zA-Z0-9]*)*"

	for elt in rcg:	
		if re.search(team_expr, elt) is not None:
			tmp = re.search(team_expr, elt).group()
			tmp = tmp.split(" ")
   			#print tmp
			return (tmp[2], tmp[3]) #team_left, team_right

	return ("notfound", "notfound")



def get_ball_data(rcg):
	"""Returns ball data for each cycle"""
	ball_data_expr = "[0-9]*[ ]\(\(b\)([ ][-]?[0-9]*(\.[0-9]*)?){4}\)"
	ball_data = list()
	#12312 ((b) -12.12312  123 123 123
	for elt in rcg:
		ball = list()		
		if re.search(ball_data_expr, elt) is not None:
			tmp = re.search(ball_data_expr, elt).group()
			tmp = tmp.split(" ")
   			#print tmp  #输出形式['6000', '((b)', '-10.7565', '34', '0', '0)']
			ball.append(int(tmp[0]))
			ball.append(float(tmp[2]))
			ball.append(float(tmp[3]))
			ball.append(float(tmp[4]))
			ball.append(float(tmp[5][:-1]))
   			#print ball #输出形式[6000, -10.7565, 34.0, 0.0, 0.0]
            		#将数据中的无用信息去除，将周期用整形表示，其他数据包括坐标等用浮点表示出来
			ball_data.append(ball) #cycle, x, y, b_v_x, b_v_y

	return ball_data



def get_kick_data(rcl, ball_data,teams):
	"""Returns kick actions for each cycle"""
	faults = get_faults(rcl, ball_data, teams)
	fault_cycle = get_faults_cycle(faults)  #获取球权转换
	#print (fault_cycle)

	goal_data = gd.get_goal_data(rcl,teams)  #进球时 [周期,球队名]
	goal_cycle = gd.get_goal_cycle(goal_data) #进球时周期
	#print (goal_cycle)
	
	half_cycle = [3000,6000,7000,8000]

	offsides = get_offsides(rcl, ball_data, teams)  #越位周期导致球权转换
	offside_cycle = get_offside_cycle(offsides)

	kick_data_expr = "Recv [a-z\-\_A-Z0-9]+([_]*[0-9]*)*:" + \
	" \(kick([ ]?[-]?[0-9][.]?)*"
	cycle_expr = "^[0-9]*" #周期匹配正则表达式
	kick_data = list()
	pre = list()
	totol = 0
	mult_num = 0	

	for elt in rcl:
		#print elt
		line = elt.split(" ")
		if len(line) > 2 and line[2] == "(kick":
			#print line
			tmp_cycle = re.search(cycle_expr, elt).group()#获取周期
			if re.search(kick_data_expr, elt): #如果匹配的数据不为空
				tmp = re.search(kick_data_expr, elt).group()
				tmp = tmp.split(" ")
   				#print "%s," % tmp #获取的数据为['Recv', 'WrightEagle_9:', '(kick', '50.4607', '-61.2677']格式
				agent = tmp[1].split("_")#将球队和球员之间的信息进行拆分，获取球员信息
				#print '%s,' % agent #获取格式为['WrightEagle', '10:']
				if len(agent) != 2:	#格式错误，如果长度大于2，将元素0和1合并为一个元素，中间用_隔开，并输出(有的球队名中间用了_)
					while len(agent) > 2:
						agent[0] += "_" + agent[1]
						del agent[1]
						#print(agent)
				#kick_data.append([int(tmp_cycle), agent[0], int(agent[1][:-1])])#合并数据 cycle, team, n°player
				new = [int(tmp_cycle) + 1, agent[0], int(agent[1][:-1])]
				if totol == 0:
					pre = [int(tmp_cycle) + 1, agent[0], int(agent[1][:-1])] #设定开始第一步为pass
					totol += 1
					mult_num = 0
					continue
				elif pre[0]+1 == new[0] and pre[1] == new[1] and pre[2] == new[2] :
					pre.append(2)  #设2为mulikick
					mult_num += 1
				elif pre[1] == new[1] and pre[2] != new[2] :
					mult_num = 0
					pre.append(0)  #设0为pass
				elif pre[1] == new[1] and pre[2] == new[2] :
					mult_num = 0
					pre.append(1)  #设1为dribble
				elif pre[1] != new[1]:
					mult_num = 0
					pre.append(4)  #设4为loss
				totol += 1
				kick_data.append(pre) #将前驱数据加入kick数据中
				if (mult_num == 0):
					kick_data.append([new[0]-1,new[1],new[2],3])
				pre = new
	#if len(new) > 2: #添加最后一个数据为未知数据
	#	kick_data.append([new[0],new[1],new[2],5])#5表示未知类型
	#比赛中发生犯规等操作时，ball_data会在同一周期内产生多组数据
	#添加标志位，在ball_data与kick_data多对一时只保留第一个数据
	#通过周期的共性合并数据，生成数据集合
	count = 0
	for elt in kick_data:
		if (elt[0] == 3000 or elt[0] == 6000 or elt[0] == 7000 ):#跳过中场产生的bug
			del elt
			continue
		flag = 0
		while count < len(ball_data):	
			if elt[0] == ball_data[count][0] and flag == 0:								
				elt.insert(3, ball_data[count][1])
				elt.insert(4, ball_data[count][2])
				elt.insert(5, ball_data[count][3])
				elt.insert(6, ball_data[count][4])				
				flag = 1
			if elt[0] == ball_data[count][0] :
				count = count - 2 #当出现多人踢球时会出现bug,这里需要数据回滚
				break
			count += 1
	e = 0
	goal_count = 0
	fault_count = 0
	half_count = 0
	offside_count = 0
	while e < len(kick_data):
		try:		
			if kick_data[e][0] == 3000 or kick_data[e][0] == 6000 or kick_data[e][0] == 7000:
				#print(kick_data[e])
				if kick_data[e-1][7] == 3:#reciver,则删除该数据
					del kick_data[e-1]
					e = e - 1 #数据回滚
				else:
					kick_data[e-1][7] = 5
				del kick_data[e] #删除不正确数据
				e = e - 1 #数据回滚
		except:
			print ("中场检测数据错误:",kick_data[e])

		if 1:
		#try:		
			if  goal_count < len(goal_cycle) and kick_data[e][0] >= goal_cycle[goal_count]:
				#print goal_cycle[goal_count]
				try:
					kick_data[e-1][7] = 6 #6表示shoot成功
				#print kick_data[e-1]
					del kick_data[e] #去除该数据reciver前驱
					e = e - 1 #数据回滚
				except:
					pass
				goal_count += 1
				#print "检测数据错误1:",kick_data[e]
		#except:
		#	print("goal检测数据错误:",kick_data[e])


		
		#try:
			elif  half_count < len(half_cycle) and kick_data[e][0] >= half_cycle[half_count]:
				try: #print(kick_data[e])
					if kick_data[e][7] == 3:#reciver,则删除该数据
						del kick_data[e]
						e = e - 1 #数据回滚
				
					kick_data[e][7] = 4 
				except:
					pass				
				half_count += 1
		#except:
		#	print ("中场检测数据错误:",kick_data[e])

		#try:
			elif  fault_count < len(fault_cycle) and kick_data[e][0] >= fault_cycle[fault_count]:
				del kick_data[e] #去除该数据reciver前驱
				e = e - 1 #数据回滚
				try:
					kick_data[e][7] = 7 #7表示fault导致球权转换
				except:
					pass				
				fault_count += 1
		#except:
		#	print("fault检测数据错误:",kick_data[e])
		#try:
			elif  offside_count < len(offside_cycle) and kick_data[e][0] >= offside_cycle[offside_count]:
				del kick_data[e] #去除该数据reciver前驱
				e = e - 1 #数据回滚
				try:
					kick_data[e][7] = 8 #8表示offside导致球权转换
				except:
					pass				
				offside_count += 1
		#except:
			#else:
			#print ("检测数据错误:",e)
		e = e + 1


    	#[ cycle , team , n , b_x , b_y ，bv_x, bv_y, flag] 共八个参数
	return kick_data



#为了方便将列表转换成map可迭代列表，提供map的第一个参数
def donothing(x):
	return x

def get_passes(kick_data):
	"""Returns passes from kick data"""

	passes = list()

	for elt in kick_data:
		if elt[7] == 0:
			passes.append(elt)
	for i in passes:
		print (i)
	return passes

def get_dribbles(kick_data):
	"""Returns dribbles from kick data"""#dribbles运球

	dribble = list()

	for elt in kick_data:
		if elt[7] == 1:
			dribble.append(elt)
	for i in dribble:
		print (i)
	return dribble

def get_multikick(kick_data):
	"""Returns multikick from kick data"""#multikicks运球

	multikick = list()

	for elt in kick_data:
		if elt[7] == 2:
			multikick.append(elt)
	for i in multikick:
		print (i)
	return multikick

def get_receive(kick_data):
	"""Returns receive kick from kick data"""#receive运球

	receive = list()

	for elt in kick_data:
		if elt[7] == 3:
			receive.append(elt)
	for i in receive:
		print (i)
	return receive

def get_lose(kick_data):
	"""Returns lose kick from kick data"""#receive运球

	lose = list()

	for elt in kick_data:
		if elt[7] == 4:
			lose.append(elt)
	for i in lose:
		print (i)
	return lose

def get_kick_types(kick_data):
	"""Return all kick types data"""
	all_types = list()
	passes = list()
	dribbles = list()
	multikickes = list()
	receives = list()
	loses = list()
	for elt in kick_data:
		if elt[7] == 0:
			passes.append(elt)
		elif elt[7] == 1:
			dribbles.append(elt)
		elif elt[7] == 2:
			multikickes.append(elt)
		elif elt[7] == 3:
			receives.append(elt)
		elif elt[7] == 4:
			loses.append(elt)
	all_types.append(passes)
	all_types.append(dribbles)
	all_types.append(multikickes)
	all_types.append(receives)
	all_types.append(loses)
	print (all_types)
	return all_types

def get_kick_chains(kick_data):
	"""Returns kick chains from kick data"""
	kick_chains = list()
	last_kick = kick_data[0]
	chain = list()
	chain.append(kick_data[0])
	sign = 0  #sign参数目的是：过滤掉动作链中只drib或者只传了一次球的动作链
	for elt in kick_data:
		
		if elt[1] == last_kick[1]:
			kick = elt
			if elt[2] == last_kick[2]:#第六个位置确定是传球还是运球
				kick.insert(5, 0) #insert "it's a dribble"
			else:
				kick.insert(5, 1) #insert "it's a pass"
				sign = sign + 1
			chain.append(elt)
		else:
			if len(chain) > 2 and sign > 1:
				kick_chains.append(chain) 
                  #将同一球队获取球的数据放入一个列表中，并将此列表作为kick_chains列表的子集
			chain = list()
			sign = 0
		last_kick = elt
	#kick_chains.append(chain)待定

	#[cycle,team,n,x,y,flag,]	 
	return kick_chains



def get_goal_self_action(kick_data,teams):
	if 1:
		sub = list() 
		goal_action = list()
		i = 0
		flag = 0
		length = len(kick_data)
		prekicker =  kick_data[0]
		while i < length:
			if kick_data[i][7] == 6:
				flag = 1  #设定标志位
				prekicker = kick_data[i] #保留前驱
				sub.append(kick_data[i])
				#print kick_data[i]
			elif kick_data[i][1] == prekicker[1] and kick_data[i][2] == prekicker[2] and flag == 1: #和前驱判断
				if kick_data[i][7] != 3:
					sub.append(kick_data[i])  #保留进球前多次self kick
			else:
				flag = 0
				if len(sub) > 0:
					goal_action.append(sub)
				sub = []
			i += 1
		#count = list()
		left_ = [teams[0],0,0,0.00]
		right_ = [teams[1],0,0,0.00]
		goal_action = sorted(goal_action, key=lambda x:x[0]) #对主列表排序
		for x in range(len(goal_action)):
		#	goal_action[x] = sorted(goal_action[x], key=lambda x:x[0])  #转置时间为正向
			print goal_action[x]
			if len(goal_action[x]) == 1:

				if goal_action[x][0][1] == teams[0]:
					left_[1] += 1
				else:
					right_[1] += 1

			speed = math.sqrt(goal_action[x][0][5]**2 + goal_action[x][0][6]**2)
			print speed
			if goal_action[x][0][1] == teams[0]:
				left_[2] += 1
				left_[3] += speed
			else:
				right_[2] += 1
				right_[3] += speed
		try:
			left_[3] = left_[3] / left_[2]
			right_[3] = right_[3] / right_[2]
		except:
			pass

		#输出处理
		file_w = open("result_goal_action.txt","a+")
		#操作数据输出
		file_w.write( "%12s\t%d\t%d\t%.2f\t%12s\t%d\t%d\t%.2f\t\n" % ( left_[0], left_[1], left_[2], left_[3], right_[0], right_[1], right_[2], right_[3] ))
		print left_
		print right_
				
	return goal_action

def get_goal_self_action_old(kick_data):
	if 1:
		sub = list() 
		goal_action = list()
		i = 0
		flag = 0
		length = len(kick_data)
		prekicker =  kick_data[0]
		while i < length:
			if kick_data[i][7] == 6:
				flag = 1  #设定标志位
				prekicker = kick_data[i] #保留前驱
				sub.append(kick_data[i])
				#print kick_data[i]
			elif kick_data[i][1] == prekicker[1] and kick_data[i][2] == prekicker[2] and flag == 1: #和前驱判断
				if kick_data[i][7] != 3:
					sub.append(kick_data[i])  #保留进球前多次self kick
			else:
				flag = 0
				if len(sub) > 0:
					goal_action.append(sub)
				sub = []
			i += 1
		
		goal_action = sorted(goal_action, key=lambda x:x[0]) #对主列表排序
		for x in range(len(goal_action)):
		#	goal_action[x] = sorted(goal_action[x], key=lambda x:x[0])  #转置时间为正向
			print goal_action[x]
	return goal_action

'''
def get_kick_chains(kick_data):
	"""Returns kick chains from kick data"""

	kick_chains = list()
	last_kick = kick_data[0]
	chain = list()
	chain.append(kick_data[0])

	for elt in kick_data:
		if elt[1] == last_kick[1]:
			kick = elt
			if elt[2] == last_kick[2]:#第六个位置确定是传球还是运球
				kick.insert(5, 0) #insert "it's a dribble"
			else:
				kick.insert(5, 1) #insert "it's a pass"
			chain.append(elt)
		else:
			if len(chain) > 1:
				kick_chains.append(chain) 
                  #将同一球队获取球的数据放入一个列表中，并将此列表作为kick_chains列表的子集
			chain = list()
		last_kick = elt

	return kick_chains
'''
def get_success_kick_chains(kick_chains,teams):
	"""Returns success kick chains from kick data"""

	success_kick_chains = list()

	for elt in kick_chains:
		#If the last kick of current chain is in penalty area
         #kick chain中最后一个数据的坐标落在罚球区
		if (elt[len(elt) - 1][3] >= 36 and elt[len(elt) - 1][3] <= 52.5 and elt[0][1] == teams[0]) or \
		(elt[len(elt) - 1][3] <= -36 and elt[len(elt) - 1][3] >= -52.5 and elt[0][1] == teams[1]):
			if elt[len(elt) - 1][4] >= -20 and elt[len(elt) - 1][4] <= 20:
				success_kick_chains.append(elt)

	return success_kick_chains

def get_corner_kicks(rcl, ball_data, teams):
	"""Returns corners"""

	corner_expr = "\(referee corner_kick_[r|l]" #l r 分别代表左右球队名称
	cycle_expr = "^[0-9]*"
	corner_kicks = list()
	flag = False

	for elt in rcl:
         #elt格式 5999,0  Recv WrightEagle_1: (attentionto our 3)(turn_neck 0.5)(say "Db1ozcQfcD")
		line = elt.split(" ") #通过空格进行拆分为列表元素
		if len(line) > 1 and line[1][:-2] == "corner_kick_":
			tmp = re.search(corner_expr, elt).group()
			tmp = tmp.split(" ")
			cycle = re.search(cycle_expr, elt).group()
			team_corner = tmp[1].split("_")
   			#print '%s ###' % team_corner #['corner', 'kick', 'r'] 
			if team_corner[2] == "r":
				team_corner = teams[1]
			else:
				team_corner = teams[0]
			corner_kicks.append([int(cycle), team_corner])
       
	for elt in corner_kicks:
		for b in list(map(donothing,ball_data)):      
			if b[0] == elt[0] and flag == False:
				#It's not the true position of the corner kick
				#the true one is in the next line
				flag = True                  
			elif flag == True and len(elt) < 4:#标志为真，且之前没有插入坐标
				elt.append(b[1])
				elt.append(b[2]) #cycle, team_corner, x, y
		flag = False
   	#print corner_kicks
	return corner_kicks 
#问题：为什么出现角球不是该数据，而是后面一个数据？
 
def get_corner_kicks_chains(kick_data, corner_kick):
	"""Returns kick chains from corner kick"""

	corner_kicks_chains = []
	tmp = []
	i = 0

	for ck in corner_kick:
		while i < len(kick_data): #存在没有查找到的数据
			if kick_data[i][0] >= ck[0]: #角球周期之后
				if kick_data[i][1] == ck[1]:#队伍相同
					for j in range(i, len(kick_data)):#在踢球的数据中查找
						if kick_data[j][1] != ck[1]:
							i = j - 1 #自己加的行，j-1之前的数据不可能再为角球，减少工作量        
							break
						else:
							tmp.append(kick_data[j]) #若为同队，链接踢球点   
       
					corner_kicks_chains.append(tmp)#把单个角球数据作为元素放在列表中                  
					tmp = []
					break
			i = i + 1
	#print corner_kicks_chains
	return corner_kicks_chains

def get_success_corner_kicks(corner_kicks_chains):
	"""Returns success kick chains from corner kicks"""

	success_corner_kicks = list()

	for elt in corner_kicks_chains:
		#If the last kick of current chain is in penalty area
		if (elt[len(elt) - 1][3] >= 36 and elt[len(elt) - 1][3] <= 52.5) or \
		(elt[len(elt) - 1][3] <= -36 and elt[len(elt) - 1][3] >= -52.5):
			if elt[len(elt) - 1][4] >= -20 and elt[len(elt) - 1][4] <= 20:
				success_corner_kicks.append(elt)
	#print success_corner_kicks
	return success_corner_kicks
#此函数可与上面的成功带球路径合并

def get_faults(rcl, ball_data, teams):
	"""Returns faults"""
	fault_expr = "\(referee foul_charge_[r|l]"
	cycle_expr = "^[0-9]*"
	faults = list()
	flag = False

	for elt in rcl:
		line = elt.split(" ")
		if len(line) > 1 and line[1][:-2] == "foul_charge_":
			tmp = re.search(fault_expr, elt).group()
			tmp = tmp.split(" ")
			cycle = re.search(cycle_expr, elt).group()
			team_fault = tmp[1].split("_") #['foul','charge','r|l']
			if(team_fault[2] == "r"):
				team_fault = teams[1]
			else:
				team_fault = teams[0]
			faults.append([int(cycle), team_fault])
	for elt in faults:
		for b in list(map(donothing,ball_data)):
			if b[0] == elt[0] and flag == False:
				#It's not the true position of the fault
				#the true one is in the next line
				flag = True
			elif flag == True and len(elt) < 4:
				elt.append(b[1])
				elt.append(b[2]) #cycle, team_fault, x, y
		flag = False

	return faults


def get_faults_cycle(faults):
	"""Returns faults cycle"""
	faults_cycle = list()
	for elt in faults:
		faults_cycle.append(elt[0])
	return faults_cycle


def get_offsides(rcl, ball_data, teams):
	"""Returns offsides"""

	offside_expr = "\(referee offside_[r|l]"
	cycle_expr = "^[0-9]*"
	offsides = list()
	flag = False

	for elt in rcl:   
		line = elt.split(" ")
		if len(line) > 1 and line[1][:-2] == "offside_":
			tmp = re.search(offside_expr, elt).group()
			tmp = tmp.split(" ")
			cycle = re.search(cycle_expr, elt).group()
			team_offside = tmp[1].split("_")
			if(team_offside[1] == "r"):
				team_offside = teams[1]
			else:
				team_offside = teams[0]
			offsides.append([int(cycle), team_offside])
	for elt in offsides:
		for b in list(map(donothing,ball_data)):
			if b[0] == elt[0] and flag == False:
				#It's not the true position of the offside
				#the true one is in the next line
				flag = True
			elif flag == True and len(elt) < 4:
				elt.append(b[1])
				elt.append(b[2]) #cycle, team_offside, x, y
		flag = False

	return offsides


def get_offside_cycle(offsides):
	"""Returns offsides cycle"""
	offside_cycle = list()
	for elt in offsides:
		offside_cycle.append(elt[0])

	return offside_cycle


def get_kick_in(rcl, ball_data, teams):
	"""Returns kick in"""# kick_in 边界球

	kick_in_expr = "\(referee kick_in_[r|l]"
	cycle_expr = "^[0-9]*"
	kick_in = list()
	flag = False

	for elt in rcl:
		line = elt.split(" ")
		if len(line) > 1 and line[1][:-2] == "kick_in_":
			tmp = re.search(kick_in_expr, elt).group()
			tmp = tmp.split(" ")
			cycle = re.search(cycle_expr, elt).group()
			team_kick_in = tmp[1].split("_")
			if(team_kick_in[2] == "r"):
				team_kick_in = teams[1]
			else:
				team_kick_in = teams[0]
			kick_in.append([int(cycle), team_kick_in])
	for elt in kick_in:
		for b in list(map(donothing,ball_data)):
			if b[0] == elt[0] and flag == False:
				#It's not the true position of the kick in
				#the true one is in the next line
				flag = True
			elif flag == True and len(elt) < 4:
				elt.append(b[1])
				elt.append(b[2]) #cycle, team_kick_in, x, y
		flag = False

	return kick_in

def get_goal_kick_data(rcl, ball_data, teams):
	"""Returns goal kicks"""#球门球

	goal_kick_expr = "\(referee goal_kick_[r|l]"
	cycle_expr = "^[0-9]*"
	goal_kicks = list()
	flag = False

	for elt in rcl:
		#if 'referee' in elt:
		#	print '%s &&&&' % elt
		line = elt.split(" ")
		if len(line) > 1 and line[1][:-2] == "goal_kick_":
			tmp = re.search(goal_kick_expr, elt).group()
			tmp = tmp.split(" ")
			cycle = re.search(cycle_expr, elt).group()
			team_goal_kick = tmp[1].split("_")
			if(team_goal_kick[2] == "r"):
				team_goal_kick = teams[1]
			else:
				team_goal_kick = teams[0]
			goal_kicks.append([int(cycle), team_goal_kick])
	for elt in goal_kicks:
		for b in list(map(donothing,ball_data)):
			if b[0] == elt[0] and flag == False:
				#It's not the true position of the goal kick
				#the true one is in the next line
				flag = True
			elif flag == True and len(elt) < 4:
				elt.append(b[1])
				elt.append(b[2]) #cycle, team_goal_kick, x, y
		flag = False

	return goal_kicks

def ball_possession(kick_chains, teams):
	"""Returns the percentage of ball possession for both teams"""

	t_left = 0
	t_right = 0
	t_total = 0

	for elt in kick_chains:
		if elt[0][1] == teams[0]:
			t_left += elt[len(elt) - 1][0] - elt[0][0] #算出持球周期
		else:
			t_right += elt[len(elt) - 1][0] - elt[0][0]
	t_total = t_left + t_right #持球总周期
	#print t_total , t_left, t_right
	t_left = float(t_left * 100) / float(t_total)
	t_right = float(t_right * 100) / float(t_total)
	tmp = str(t_left) #小数点前后拆分，进位操作
	tmp = tmp.split(".")
	if int(tmp[1][0]) >= 5:
		t_left = int(tmp[0]) + 1
	else:
		t_left = int(tmp[0])
	tmp = str(t_right)
	tmp = tmp.split(".")
	if int(tmp[1][0]) >= 5:
		t_right = int(tmp[0]) + 1
	else:
		t_right = int(tmp[0])
	ball_possession = (t_left, t_right)

	return ball_possession

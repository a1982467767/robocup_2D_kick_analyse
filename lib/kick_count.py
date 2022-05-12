#!/usr/bin/python
#-*-coding:utf-8-*

"""
Copyright (C) 2018 SunChen
"""
import os 
import math

pwd = os.getcwd()
result = "/result/" 
result_file = "kickAngleCount"

def getOriginData(time_str, save_path, area):
	file_r = open(save_path + "/" + result_file + str(area) + ".txt","r")
	content = file_r.read()
	file_r.close()
	content = content.split("\n")
	origin = list()
	for elt in content:
		#print (elt)
		elt=elt.split("\t")
		if len(elt) == 1: #去=====
			continue
		if elt[0] == '':#去空行
			continue
		if elt[1] == 'kicks':#去标题
			continue
		elt[1] = float(elt[1])
		elt[2] = float(elt[2])
		elt[3] = float(elt[3])
		elt[4] = float(elt[4])
		elt[5] = float(elt[5])
		elt[6] = float(elt[6])	
		elt[7] = float(elt[7])
		elt[8] = float(elt[8])
		elt[9] = float(elt[9])	
		elt[10] = float(elt[10])
		try:
			elt[11] = float(elt[11])
		except:
			elt[11] = float(elt[11].split("/")[0])			 
		#print (elt)
		origin.append(elt)
		#['HfutEngine2018', '279', '143', '83.87', '16.13', '15.77', '19.35', '64.87', '1']
		#"team","kick","mulkick","forward","back","less0.5","0.5~0.8","high0.8","goal"
	#print (origin)
	return origin



def sortByName(data_set):  #这里对各队进行排序
	data_set1 = list()
	try:
		for elt in data_set:
			elt = sorted(elt, key=lambda x:x[0],reverse=True) #对字列表排序
			data_set1.append(elt)
		data_set1 = sorted(data_set1, key=lambda x:(x[0][0],x[1][0])) #对主列表排序
		#for elt1 in data_set1:  #通过排序,可使得yushan永远在数据的右边
		#	print (elt1)
	except :
		print (elt)
	return data_set1
	
def countAvgData(data_set):
	length = len(data_set)
	i = 1
	count = 1	
	new_count = data_set[0]
	avg = list()
	count_list = list()
	left_zero_count = 0
	right_zero_count = 0
	while i  < length :
		#print (data_set[i])
		if new_count[0][0] == data_set[i][0][0] and new_count[1][0] == data_set[i][1][0]:
			#上下两组数 左右队相同 数据叠加
			new_count = addData(new_count,data_set[i])
			count += 1
			#print data_set[i]
			if data_set[i][0][1] < 2:
				left_zero_count += 1
			if data_set[i][1][1] < 2:
				right_zero_count += 1
		else:
			#print (new_count,count)
			avg.append(avgData(new_count,count,left_zero_count,right_zero_count))
			count_list.append(count)
			new_count = data_set[i]
			count = 1
			left_zero_count = 0
			right_zero_count = 0
		i += 1
	avg.append(avgData(new_count,count,left_zero_count,right_zero_count))
	count_list.append(count)
	#取同一队名的所有数据平均值
	new_acount = avg[0]
	ax = 1
	count = 1
	left_zero_count = 0
	right_zero_count = 0
	org_avg_len = len(avg)
	while ax < org_avg_len :
		if avg[ax][0][0] == new_acount[0][0] :
			new_acount = addData1(new_acount,avg[ax])
			count += 1
			if avg[ax][0][1] < 2:
				left_zero_count += 1
			if avg[ax][1][1] < 2:
				right_zero_count += 1
		else :
			avg.append(avgData1(new_acount,count,left_zero_count,right_zero_count))
			count_list.append(count)
			new_acount = avg[ax]
			count = 1
			left_zero_count = 0
			right_zero_count = 0
		ax += 1
	avg.append(avgData1(new_acount,count,left_zero_count,right_zero_count))
	count_list.append(count)
	#for e in avg:
	#	print (e)
	return avg,count_list
		
#数据相加				
def addData(new_count,elt_data_set):  
	new = [[new_count[0][0], new_count[0][1] + elt_data_set[0][1], \
		new_count[0][2] + elt_data_set[0][2], new_count[0][3] + elt_data_set[0][3], \
		new_count[0][4] + elt_data_set[0][4], new_count[0][5] + elt_data_set[0][5], \
		new_count[0][6] + elt_data_set[0][6], new_count[0][7] + elt_data_set[0][7], \
		new_count[0][8] + elt_data_set[0][8], new_count[0][9] + elt_data_set[0][9], \
		new_count[0][10] + elt_data_set[0][10], new_count[0][11] + elt_data_set[0][11],\
		new_count[0][12] + elt_data_set[0][12]],\
	[new_count[1][0], new_count[1][1] + elt_data_set[1][1], \
		new_count[1][2] + elt_data_set[1][2], new_count[1][3] + elt_data_set[1][3], \
		new_count[1][4] + elt_data_set[1][4], new_count[1][5] + elt_data_set[1][5], \
		new_count[1][6] + elt_data_set[1][6], new_count[1][7] + elt_data_set[1][7], \
		new_count[1][8] + elt_data_set[1][8], new_count[1][9] + elt_data_set[1][9], \
		new_count[1][10] + elt_data_set[1][10], new_count[1][11] + elt_data_set[1][11],\
		new_count[1][12] + elt_data_set[1][12]]]
	#print (new)
	return new

#数据相加1			
def addData1(new_count,elt_data_set):  
	new = [[new_count[0][0], new_count[0][1] + elt_data_set[0][1], \
		new_count[0][2] + elt_data_set[0][2], new_count[0][3] + elt_data_set[0][3], \
		new_count[0][4] + elt_data_set[0][4], new_count[0][5] + elt_data_set[0][5], \
		new_count[0][6] + elt_data_set[0][6], new_count[0][7] + elt_data_set[0][7], \
		new_count[0][8] + elt_data_set[0][8], new_count[0][9] + elt_data_set[0][9], \
		new_count[0][10] + elt_data_set[0][10], new_count[0][11] + elt_data_set[0][11],\
		new_count[0][12] + elt_data_set[0][12]],\
	["ALLTeams", new_count[1][1] + elt_data_set[1][1], \
		new_count[1][2] + elt_data_set[1][2], new_count[1][3] + elt_data_set[1][3], \
		new_count[1][4] + elt_data_set[1][4], new_count[1][5] + elt_data_set[1][5], \
		new_count[1][6] + elt_data_set[1][6], new_count[1][7] + elt_data_set[1][7], \
		new_count[1][8] + elt_data_set[1][8], new_count[1][9] + elt_data_set[1][9], \
		new_count[1][10] + elt_data_set[1][10], new_count[1][11] + elt_data_set[1][11],\
		new_count[1][12] + elt_data_set[1][12]]]
	#print (new)
	return new

#数据相减				
def desData(new_count,elt_data_set):  
	new = [[new_count[0][0], new_count[0][1] - elt_data_set[0][1], new_count[0][2] - elt_data_set[0][2], new_count[0][3] - elt_data_set[0][3], new_count[0][4] - elt_data_set[0][4], new_count[0][5] - elt_data_set[0][5], new_count[0][6] - elt_data_set[0][6], new_count[0][7] - elt_data_set[0][7], new_count[0][8] - elt_data_set[0][8], new_count[0][9] - elt_data_set[0][9], new_count[0][10] - elt_data_set[0][10], new_count[0][11] - elt_data_set[0][11]],
		   [new_count[1][0], new_count[1][1] - elt_data_set[1][1], new_count[1][2] - elt_data_set[1][2], new_count[1][3] - elt_data_set[1][3], new_count[1][4] - elt_data_set[1][4], new_count[1][5] - elt_data_set[1][5], new_count[1][6] - elt_data_set[1][6], new_count[1][7] - elt_data_set[1][7], new_count[1][8] - elt_data_set[1][8], new_count[1][9] - elt_data_set[1][9], new_count[1][10] - elt_data_set[1][10], new_count[1][11] - elt_data_set[1][11]]]
	#print (new)
	return new

#数据相减1				
def desData1(new_count,elt_data_set):  
	new = [[new_count[0][0], new_count[0][1] - elt_data_set[0][1], new_count[0][2] - elt_data_set[0][2], new_count[0][3] - elt_data_set[0][3], new_count[0][4] - elt_data_set[0][4], new_count[0][5] - elt_data_set[0][5], new_count[0][6] - elt_data_set[0][6], new_count[0][7] - elt_data_set[0][7], new_count[0][8] - elt_data_set[0][8], new_count[0][9] - elt_data_set[0][9], new_count[0][10] - elt_data_set[0][10], new_count[0][11] - elt_data_set[0][11]],
	["ALLTeams", new_count[1][1] - elt_data_set[1][1], new_count[1][2] - elt_data_set[1][2], new_count[1][3] - elt_data_set[1][3], new_count[1][4] - elt_data_set[1][4], new_count[1][5] - elt_data_set[1][5], new_count[1][6] - elt_data_set[1][6], new_count[1][7] - elt_data_set[1][7], new_count[1][8] - elt_data_set[1][8], new_count[1][9] - elt_data_set[1][9], new_count[1][10] - elt_data_set[1][10], new_count[1][11] - elt_data_set[1][11]]]
	#print (new)
	return new

#数据相乘				
def multiData(new_count,elt_data_set):  
	new = [[new_count[0][0], new_count[0][1] * elt_data_set[0][1], new_count[0][2] * elt_data_set[0][2], new_count[0][3] * elt_data_set[0][3], new_count[0][4] * elt_data_set[0][4], new_count[0][5] * elt_data_set[0][5], new_count[0][6] * elt_data_set[0][6], new_count[0][7] * elt_data_set[0][7], new_count[0][8] * elt_data_set[0][8], new_count[0][9] * elt_data_set[0][9], new_count[0][10] * elt_data_set[0][10], new_count[0][11] * elt_data_set[0][11]],
	[new_count[1][0], new_count[1][1] * elt_data_set[1][1], new_count[1][2] * elt_data_set[1][2], new_count[1][3] * elt_data_set[1][3], new_count[1][4] * elt_data_set[1][4], new_count[1][5] * elt_data_set[1][5], new_count[1][6] * elt_data_set[1][6], new_count[1][7] * elt_data_set[1][7], new_count[1][8] * elt_data_set[1][8],new_count[1][9] * elt_data_set[1][9], new_count[1][10] * elt_data_set[1][10], new_count[1][11] * elt_data_set[1][11]]]
	#print (new)
	return new

#数据相乘1				
def multiData1(new_count,elt_data_set):  
	new = [[new_count[0][0], new_count[0][1] * elt_data_set[0][1], new_count[0][2] * elt_data_set[0][2], new_count[0][3] * elt_data_set[0][3], new_count[0][4] * elt_data_set[0][4], new_count[0][5] * elt_data_set[0][5], new_count[0][6] * elt_data_set[0][6], new_count[0][7] * elt_data_set[0][7], new_count[0][8] * elt_data_set[0][8], new_count[0][9] * elt_data_set[0][9], new_count[0][10] * elt_data_set[0][10], new_count[0][11] * elt_data_set[0][11]],
	["ALLTeams", new_count[1][1] * elt_data_set[1][1], new_count[1][2] * elt_data_set[1][2], new_count[1][3] * elt_data_set[1][3], new_count[1][4] * elt_data_set[1][4], new_count[1][5] * elt_data_set[1][5], new_count[1][6] * elt_data_set[1][6], new_count[1][7] * elt_data_set[1][7], new_count[1][8] * elt_data_set[1][8],new_count[1][9] * elt_data_set[1][9], new_count[1][10] * elt_data_set[1][10], new_count[1][11] * elt_data_set[1][11]]]
	#print (new)
	return new

#平方
def pow2Data(new_count):  
	new = [[new_count[0][0], new_count[0][1] ** 2, new_count[0][2] ** 2, new_count[0][3] ** 2, new_count[0][4] ** 2, new_count[0][5] ** 2, new_count[0][6] ** 2, new_count[0][7] ** 2, new_count[0][8] ** 2, new_count[0][9] ** 2, new_count[0][10] ** 2, new_count[0][11] ** 2],[new_count[1][0], new_count[1][1] ** 2, new_count[1][2] ** 2, new_count[1][3] ** 2, new_count[1][4] ** 2, new_count[1][5] ** 2, new_count[1][6] ** 2, new_count[1][7] ** 2, new_count[1][8] ** 2, new_count[1][9] ** 2, new_count[1][10] ** 2, new_count[1][11] ** 2]]
	#print (new)
	return new


def sqrtData(new_count):  
	new = [[new_count[0][0], math.sqrt(new_count[0][1]),math.sqrt(new_count[0][2]), math.sqrt(new_count[0][3]), math.sqrt(new_count[0][4]), math.sqrt(new_count[0][5]), math.sqrt(new_count[0][6]), math.sqrt(new_count[0][7]), math.sqrt(new_count[0][8]), math.sqrt(new_count[0][9]), math.sqrt(new_count[0][10]), math.sqrt(new_count[0][11])],
	[new_count[1][0], math.sqrt(new_count[1][1]),math.sqrt(new_count[1][2]), math.sqrt(new_count[1][3]), math.sqrt(new_count[1][4]), math.sqrt(new_count[1][5]), math.sqrt(new_count[1][6]), math.sqrt(new_count[1][7]), math.sqrt(new_count[1][8]), math.sqrt(new_count[1][9]), math.sqrt(new_count[1][10]), math.sqrt(new_count[1][11])]]
	#print (new)
	return new

#数据取平均值
def avgData(new_count,count,left_zero_count,right_zero_count):

	count_l = count - left_zero_count
	count_r = count - right_zero_count
	new = [ [new_count[0][0], round(new_count[0][1]/count_l,2), round(new_count[0][2]/count_l,2), \
			round(new_count[0][3]/count_l,2), round(new_count[0][4]/count_l,2), \
			round(new_count[0][5]/count_l,2), round(new_count[0][6]/count_l,2), \
			round(new_count[0][7]/count_l,2), round(new_count[0][8]/count_l,2), \
			round(new_count[0][9]/count_l,2), round(new_count[0][10]/count_l,2),\
			round(new_count[0][11]/count,2),round(new_count[0][12]/count,2)],
		[new_count[1][0], round(new_count[1][1]/count_r,2), round(new_count[1][2]/count_r,2), \
			round(new_count[1][3]/count_r,2), round(new_count[1][4]/count_r,2), \
			round(new_count[1][5]/count_r,2), round(new_count[1][6]/count_r,2), \
			round(new_count[1][7]/count_r,2), round(new_count[1][8]/count_r,2), \
			round(new_count[1][9]/count_r,2), round(new_count[1][10]/count_r,2),\
			round(new_count[1][11]/count,2),round(new_count[1][12]/count,2)] ]
	#print (new)
	return new

#数据取平均值
def avgData1(new_count,count,left_zero_count,right_zero_count):

	count_l = count - left_zero_count
	count_r = count - right_zero_count
	new = [ [new_count[0][0], round(new_count[0][1]/count_l,2), round(new_count[0][2]/count_l,2), \
			round(new_count[0][3]/count_l,2), round(new_count[0][4]/count_l,2), \
			round(new_count[0][5]/count_l,2), round(new_count[0][6]/count_l,2), \
			round(new_count[0][7]/count_l,2), round(new_count[0][8]/count_l,2), \
			round(new_count[0][9]/count_l,2), round(new_count[0][10]/count_l,2),\
			round(new_count[0][11]/count,2),round(new_count[0][12]/count,2)],
		["ALLTeams", round(new_count[1][1]/count_r,2), round(new_count[1][2]/count_r,2), \
			round(new_count[1][3]/count_r,2), round(new_count[1][4]/count_r,2), \
			round(new_count[1][5]/count_r,2), round(new_count[1][6]/count_r,2), \
			round(new_count[1][7]/count_r,2), round(new_count[1][8]/count_r,2), \
			round(new_count[1][9]/count_r,2), round(new_count[1][10]/count_r,2),\
			round(new_count[1][11]/count,2),round(new_count[1][12]/count,2)] ]
	#print (new)
	return new


#队内标准差
def intStdDev(data_set,avg_data):
	length = len(data_set)
	i = 1
	count = 1
	num = 0	
	new_count = desData(data_set[0],data_set[0])  #初始化
	#print (new_count,avg_data[num])
	IntStdDev = list() #记录标准差
	count_list = list() #记录总场数
	while i  < length :
		#print (data_set[i])
		if new_count[0][0] == data_set[i][0][0] and new_count[1][0] == data_set[i][1][0]:
			#上下两组数 左右队相同 数据叠加
			new_count = addData(new_count,pow2Data(desData(data_set[i],avg_data[num])))  #取差值 平方再相加
			count += 1
		else:
			#print (new_count,count)
			new_count = sqrtData(new_count)  #开方
			IntStdDev.append(avgData(new_count,count)) #取1/n即取平均值
			count_list.append(count)
			new_count = desData(data_set[i],data_set[i])
			count = 1
			num += 1
		i += 1
	new_count = sqrtData(new_count)  #开方
	IntStdDev.append(avgData(new_count,count)) #取1/n即取平均值
	count_list.append(count)
	#for x in IntStdDev:
	#	print(x)
	return IntStdDev,count_list

def kick_anl(time_str, save_path):
	for area in range(8):
		origin_data = getOriginData(time_str, save_path, area)
		length = len(origin_data)
		data_set = list()
		i = 0
		while(i < length):
			#计算分值
			data_part = [origin_data[i],origin_data[i + 1]]
			if (origin_data[i][11] > origin_data[i + 1][11]):
				data_part[0].append(3.0)
				data_part[1].append(0.0)
			elif (origin_data[i][11] == origin_data[i + 1][11]):
				data_part[0].append(1.0)
				data_part[1].append(1.0)			
			else:
				data_part[0].append(0.0)
				data_part[1].append(3.0)
			data_set.append(data_part)
			i += 2

		data_set = sortByName(data_set)
		avg_data,count_list_avg= countAvgData(data_set)
		#平均值数据写入
		if os.path.exists(pwd + result + time_str + "/avgKickAngleCount"+ str(area) + ".txt"):
			os.remove(pwd + result + time_str + "/avgKickAngleCount"+ str(area) + ".txt")#删除
		file_w = open(pwd + result + time_str + "/avgKickAngleCount"+ str(area) + ".txt","a+")

		file_w.write( "%12s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n" % \
						("team","kick","pass","dribble","hold","forward","less0.5","high0.8","goal","win","all") )
		file_w.write("=" * 108 + "\n")
		i = 0
		totol = [0,0]
		for avge in avg_data:
			totol[0] = avge[0][2]+avge[0][3]+avge[0][4]
			totol[1] = avge[1][2]+avge[1][3]+avge[1][4]
			try:
				file_w.write( "%12s\t%.2f\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f\t%.2f%%\t%d\n" % \
					( avge[0][0],totol[0],avge[0][2]/totol[0],avge[0][3]/totol[0],avge[0][4]/totol[0],\
					  avge[0][6],avge[0][8],avge[0][10],avge[0][11],avge[0][12]/3.0,count_list_avg[i]))
			except:
				file_w.write( "%12s\t%.2f\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f\t%.2f%%\t%d\n" % \
					( avge[0][0], 0, 0.0, 0.0, 0.0, avge[0][6],avge[0][8],\
					  avge[0][10],avge[0][11],avge[0][12]/3.0,count_list_avg[i]) )
			try:
				file_w.write( "%12s\t%.2f\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f\t%.2f%%\t%d\n" % \
					( avge[1][0],totol[1],avge[1][2]/totol[1],avge[1][3]/totol[1],avge[1][4]/totol[1],\
					  avge[1][6],avge[1][8],avge[1][10],avge[1][11],avge[1][12]/3.0,count_list_avg[i]) )
				file_w.write("=" * 108 + "\n")
			except:
				file_w.write( "%12s\t%.2f\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f\t%.2f%%\t%d\n" % \
					( avge[1][0], 0, 0.0, 0.0, 0.0, avge[1][6],avge[1][8],\
					  avge[1][10],avge[1][11],avge[1][12]/3.0,count_list_avg[i]) )
				file_w.write("=" * 108 + "\n") 
			i += 1
		file_w.close()
		print ("平均值数据写入:"+ pwd + result + time_str + "/avgKickAngleCount"+ str(area) + ".txt" + "成功...")
		'''
		intStdDev_data,count_list_isd = intStdDev(data_set,avg_data)
		#标准差数据写入
		if 0:
			if os.path.exists(pwd + result + time_str + "/intStdDevKickAngleCount"+ str(area) + ".txt"):
				os.remove(pwd + result + time_str + "/intStdDevKickAngleCount"+ str(area) + ".txt")#删除
			file_w = open(pwd + result + time_str + "/intStdDevKickAngleCount.txt"+ str(area) + ".txt")
			file_w.write( "%12s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n" % \
							("team","reciver","passes","dribble","mulkick","loses","forward","less0.5","0.5~0.8","high0.8","goal","all") )
			file_w.write("==" * 100 + "\n")
			ai = 0
			for avge in intStdDev_data:
				file_w.write( "%12s\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f\t%d\n" % \
					( avge[0][0],avge[0][1],avge[0][2],avge[0][3],avge[0][4],avge[0][5],avge[0][6],avge[0][8],avge[0][9],avge[0][10],avge[0][11],count_list_isd[ai] ))
				file_w.write( "%12s\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f\t%d\n" % \
					( avge[1][0],avge[1][1],avge[1][2],avge[1][3],avge[1][4],avge[1][5],avge[1][6],avge[1][8],avge[1][9],avge[1][10],avge[1][11],count_list_isd[ai] ))
				file_w.write("==" * 100 + "\n")
				ai += 1
			file_w.close()
			print ("标准差数据写入:"+ pwd + result + time_str + "/intStdDevKickAngleCount"+ str(area) + ".txt"+"成功...")
		'''


def kick_anl_all():
	time_str = '/All_Data'
	save_path = 'All_Data'
	for area in range(8):
		#print area
		origin_data = getOriginData(time_str, save_path, area)	
		length = len(origin_data)
		data_set = list()
		i = 0
		while(i < length):
			#计算分值
			data_part = [origin_data[i],origin_data[i + 1]]
			if (origin_data[i][11] > origin_data[i + 1][11]):
				data_part[0].append(3.0)
				data_part[1].append(0.0)
			elif (origin_data[i][11] == origin_data[i + 1][11]):
				data_part[0].append(1.0)
				data_part[1].append(1.0)			
			else:
				data_part[0].append(0.0)
				data_part[1].append(3.0)
			data_set.append(data_part)
			i += 2
		#print (data_set)
		#data_set = sortByName(data_set)
		data_set = sorted(data_set, key=lambda x:(x[0][0],x[1][0])) #对主列表排序
		avg_data,count_list_avg= countAvgData(data_set)
		#intStdDev_data,count_list_isd = intStdDev(data_set,avg_data)
		#平均值数据写入
		if os.path.exists(pwd + time_str + "/avgKickAngleCount" + str(area) + ".txt"):
			os.remove(pwd + time_str + "/avgKickAngleCount" + str(area) + ".txt")#删除
		file_w = open(pwd + time_str + "/avgKickAngleCount" + str(area) + ".txt","a+")
		file_w.write( "%12s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n" % \
						("team","kicks","pass","dribble","hold","forward","less0.5","high0.8","goal","win","all") )
		file_w.write("=" * 108 + "\n")
		i = 0
		totol = [0,0]
		for avge in avg_data:
			totol[0] = avge[0][2]+avge[0][3]+avge[0][4]
			totol[1] = avge[1][2]+avge[1][3]+avge[1][4]
			try:
				file_w.write( "%12s\t%.2f\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f\t%.2f%%\t%d\n" % \
					( avge[0][0],totol[0],avge[0][2]/totol[0],avge[0][3]/totol[0],avge[0][4]/totol[0],\
					  avge[0][6],avge[0][8],avge[0][10],avge[0][11],avge[0][12]/3.0,count_list_avg[i]))
			except:
				file_w.write( "%12s\t%.2f\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f\t%.2f%%\t%d\n" % \
					( avge[0][0], 0, 0.0, 0.0, 0.0, avge[0][6],avge[0][8],\
					  avge[0][10],avge[0][11],avge[0][12]/3.0,count_list_avg[i]) )
			try:
				file_w.write( "%12s\t%.2f\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f\t%.2f%%\t%d\n" % \
					( avge[1][0],totol[1],avge[1][2]/totol[1],avge[1][3]/totol[1],avge[1][4]/totol[1],\
					  avge[1][6],avge[1][8],avge[1][10],avge[1][11],avge[1][12]/3.0,count_list_avg[i]) )
				file_w.write("=" * 108 + "\n")
			except:
				file_w.write( "%12s\t%.2f\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f\t%.2f%%\t%d\n" % \
					( avge[1][0], 0, 0.0, 0.0, 0.0, avge[1][6],avge[1][8],\
					  avge[1][10],avge[1][11],avge[1][12]/3.0,count_list_avg[i]) )
				file_w.write("=" * 108 + "\n") 
			i += 1
		file_w.close()
		print ("平均值数据写入:" + pwd + time_str + "/avgKickAngleCount" + str(area) + ".txt" + "成功...")



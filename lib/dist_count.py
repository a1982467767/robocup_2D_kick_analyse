#!/usr/bin/python
#-*-coding:utf-8-*

"""
Copyright (C) 2018 SunChen
"""
import os 
import math

pwd = os.getcwd()
result = "/result/" 
result_file = "kickdataByDist"

def getOriginData(time_str, save_path, area):
	mydir = os.path.abspath(save_path + "/" + result_file + str(area) + ".txt")
	print mydir
	file_r = open(save_path + "/" + result_file + str(area) + ".txt","r")
	content = file_r.read()
	file_r.close()
	content = content.split("\n")
	origin = list()
	for elt in content:
		#print (elt)
		elt = elt.split("\t")
		if elt[0] == '':#去空行
			continue
		elt[1] = float(elt[1])
		elt[2] = float(elt[2])
		elt[3] = float(elt[3])
		elt[4] = float(elt[4])
		elt[5] = float(elt[5])
		elt[6] = float(elt[6])	
		elt[7] = float(elt[7])
		elt[8] = float(elt[8])
		try:
			elt[9] = float(elt[9])
		except:
			elt[9] = float(elt[9].split("/")[0])			 

		origin.append(elt)

	#print (origin)
	return origin



def sortByName(data_set):  #这里对各队进行排序
	data_set1 = list()
	for elt in data_set:
		elt = sorted(elt, key=lambda x:x[0],reverse=True) #对字列表排序
		data_set1.append(elt)
	data_set1 = sorted(data_set1, key=lambda x:(x[0][0],x[1][0])) #对主列表排序
	#for elt1 in data_set1:  #通过排序,可使得yushan永远在数据的右边
	#	print (elt1)
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
			#去除0数据
			try:
				if data_set[i][0][1] + data_set[i][0][2] + data_set[i][0][3] + \
					data_set[i][0][4] + data_set[i][0][5] + data_set[i][0][6] + \
					data_set[i][0][7] + data_set[i][0][8] < 1.0:
					left_zero_count += 1
				if data_set[i][1][1] + data_set[i][1][2] + data_set[i][1][3] + \
					data_set[i][1][4] + data_set[i][1][5] + data_set[i][1][6] + \
					data_set[i][1][7] + data_set[i][1][8] < 1.0:
					right_zero_count += 1
			except:
				print dataset[i]
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

	#同一主队名再取总平均值
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
			#去除0数据，不等于1为不合法的数据，这里要去除掉
			if avg[ax][0][1] + avg[ax][0][2] + avg[ax][0][3] + \
				avg[ax][0][4] + avg[ax][0][5] + avg[ax][0][6] + \
				avg[ax][0][7] + avg[ax][0][8] < 1.0: 
				left_zero_count += 1
			if avg[ax][1][1] + avg[ax][1][2] + avg[ax][1][3] + \
				avg[ax][1][4] + avg[ax][1][5] + avg[ax][1][6] + \
				avg[ax][1][7] + avg[ax][1][8] < 1.0:
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
	new = [[new_count[0][0], new_count[0][1] + elt_data_set[0][1], new_count[0][2] + elt_data_set[0][2], new_count[0][3] + elt_data_set[0][3], new_count[0][4] + elt_data_set[0][4], new_count[0][5] + elt_data_set[0][5], new_count[0][6] + elt_data_set[0][6], new_count[0][7] + elt_data_set[0][7], new_count[0][8] + elt_data_set[0][8], new_count[0][9] + elt_data_set[0][9]],
	[new_count[1][0], new_count[1][1] + elt_data_set[1][1], new_count[1][2] + elt_data_set[1][2], new_count[1][3] + elt_data_set[1][3], new_count[1][4] + elt_data_set[1][4], new_count[1][5] + elt_data_set[1][5], new_count[1][6] + elt_data_set[1][6], new_count[1][7] + elt_data_set[1][7], new_count[1][8] + elt_data_set[1][8], new_count[1][9] + elt_data_set[1][9]]]
	#print (new)
	return new

#数据相加1			
def addData1(new_count,elt_data_set):  
	new = [[new_count[0][0], new_count[0][1] + elt_data_set[0][1], new_count[0][2] + elt_data_set[0][2], new_count[0][3] + elt_data_set[0][3], new_count[0][4] + elt_data_set[0][4], new_count[0][5] + elt_data_set[0][5], new_count[0][6] + elt_data_set[0][6], new_count[0][7] + elt_data_set[0][7], new_count[0][8] + elt_data_set[0][8], new_count[0][9] + elt_data_set[0][9]],
	["ALLTeams", new_count[1][1] + elt_data_set[1][1], new_count[1][2] + elt_data_set[1][2], new_count[1][3] + elt_data_set[1][3], new_count[1][4] + elt_data_set[1][4], new_count[1][5] + elt_data_set[1][5], new_count[1][6] + elt_data_set[1][6], new_count[1][7] + elt_data_set[1][7], new_count[1][8] + elt_data_set[1][8], new_count[1][9] + elt_data_set[1][9]]]
	#print (new)
	return new


#数据取平均值
def avgData(new_count,count,left_zero_count,right_zero_count):

	count_l = count - left_zero_count
	count_r = count - right_zero_count
	new = [ [new_count[0][0], round(new_count[0][1]/count_l,2), round(new_count[0][2]/count_l,2), \
			round(new_count[0][3]/count_l,2), round(new_count[0][4]/count_l,2), \
			round(new_count[0][5]/count_l,2), round(new_count[0][6]/count_l,2), \
			round(new_count[0][7]/count_l,2), round(new_count[0][8]/count_l,2), round(new_count[0][9]/count,2)],
		[new_count[1][0], round(new_count[1][1]/count_r,2), round(new_count[1][2]/count_r,2), \
			round(new_count[1][3]/count_r,2), round(new_count[1][4]/count_r,2), \
			round(new_count[1][5]/count_r,2), round(new_count[1][6]/count_r,2), \
			round(new_count[1][7]/count_r,2), round(new_count[1][8]/count_r,2), round(new_count[1][9]/count,2)]]
	#print (new)
	return new

#数据取平均值
def avgData1(new_count,count,left_zero_count,right_zero_count):

	count_l = count - left_zero_count
	count_r = count - right_zero_count
	new = [ [new_count[0][0], round(new_count[0][1]/count_l,2), round(new_count[0][2]/count_l,2), \
			round(new_count[0][3]/count_l,2), round(new_count[0][4]/count_l,2), \
			round(new_count[0][5]/count_l,2), round(new_count[0][6]/count_l,2), \
			round(new_count[0][7]/count_l,2), round(new_count[0][8]/count_l,2), round(new_count[0][9]/count,2)],
		["ALLTeams", round(new_count[1][1]/count_r,2), round(new_count[1][2]/count_r,2), \
			round(new_count[1][3]/count_r,2), round(new_count[1][4]/count_r,2), \
			round(new_count[1][5]/count_r,2), round(new_count[1][6]/count_r,2), \
			round(new_count[1][7]/count_r,2), round(new_count[1][8]/count_r,2), round(new_count[1][9]/count,2)]]
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
			data_part = [origin_data[i],origin_data[i + 1]]
			i += 2
			data_set.append(data_part)
		data_set = sortByName(data_set)
		avg_data,count_list_avg= countAvgData(data_set)
		#intStdDev_data,count_list_isd = intStdDev(data_set,avg_data)
		#平均值数据写入
		if os.path.exists(pwd + result + time_str + "/avgkickdataByDist" + str(area) + ".txt"):
			os.remove(pwd + result + time_str + "/avgkickdataByDist" + str(area) + ".txt")#删除
		file_w = open(pwd + result + time_str + "/avgkickdataByDist" + str(area) + ".txt","a+")
		file_w.write( "%12s\t%4s\t%4s\t%4s\t%4s\t%4s\t%4s\t%4s\t%4s\t%4s\t%4s\t\n" % \
						("team","0.3","0.4","0.5","0.6","0.7","0.8","0.9","1.0","goal","all") )
		file_w.write("=" * 92 + "\n")
		i = 0
		totol = [0,0]
		for avge in avg_data:
			file_w.write( "%12s\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%d\n" % \
				( avge[0][0],avge[0][1],avge[0][2],avge[0][3],avge[0][4],avge[0][5],avge[0][6],avge[0][7],avge[0][8],avge[0][9],count_list_avg[i]))
			file_w.write( "%12s\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%d\n" % \
				( avge[1][0],avge[1][1],avge[1][2],avge[1][3],avge[1][4],avge[1][5],avge[1][6],avge[0][7],avge[1][8],avge[1][9],count_list_avg[i]))
			file_w.write("=" * 92 + "\n")
			i += 1
		file_w.close()
		print ("平均值数据写入:"+ pwd + result + time_str + "/avgkickdataByDist" + str(area) + ".txt" +"成功...")


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
			data_part = [origin_data[i],origin_data[i + 1]]
			i += 2
			data_set.append(data_part)
		data_set = sorted(data_set, key=lambda x:(x[0][0],x[1][0])) #对主列表排序
		#data_set = sortByName(data_set)
		avg_data,count_list_avg= countAvgData(data_set)
		#intStdDev_data,count_list_isd = intStdDev(data_set,avg_data)
		#平均值数据写入
		if os.path.exists(pwd + time_str + "/avgkickdataByDist" + str(area) + ".txt"):
			os.remove(pwd + time_str + "/avgkickdataByDist" + str(area) + ".txt")#删除
		file_w = open(pwd + time_str + "/avgkickdataByDist" + str(area) + ".txt","a+")
		file_w.write( "%12s\t%4s\t%4s\t%4s\t%4s\t%4s\t%4s\t%4s\t%4s\t%4s\t%4s\t\n" % \
						("team","0.3","0.4","0.5","0.6","0.7","0.8","0.9","1.0","goal","all") )
		file_w.write("=" * 94 + "\n")
		i = 0
		totol = [0,0]
		for avge in avg_data:
			file_w.write( "%12s\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%d\n" % \
				( avge[0][0],avge[0][1],avge[0][2],avge[0][3],avge[0][4],avge[0][5],avge[0][6],avge[0][7],avge[0][8],avge[0][9],count_list_avg[i]))
			file_w.write( "%12s\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%d\n" % \
				( avge[1][0],avge[1][1],avge[1][2],avge[1][3],avge[1][4],avge[1][5],avge[1][6],avge[0][7],avge[1][8],avge[1][9],count_list_avg[i]))
			file_w.write("=" * 94 + "\n")
			i += 1
		file_w.close()
		print ("平均值数据写入:" + pwd + time_str + "/avgkickdataByDist" + str(area) + ".txt" + "成功...")

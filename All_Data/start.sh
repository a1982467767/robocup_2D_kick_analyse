#!/bin/bash

# 一个用于kick data 数据的可视化画图工具
# Qian Jipeng(C) Sunc

cd All_Data

python3 ./lib/plot.py
echo data preprocess ok!

echo start to draw single area images
cd ./result

for team in $(ls *)
do
		
	echo "$team"
	
	for area in 0 1 2 3 4 5 6 7
	
	do
		python3 ../lib/draw_mul.py $team $area $team
		echo $team $area has been drawed!
	done
	python3 ../lib/imageCompose.py $team
	python3 ../lib/soccerplayer.py $team

done

echo single images ok!

echo image composed ok!


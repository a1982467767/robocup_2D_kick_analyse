#!/bin/sh
#Copyright (C) 2018 YuShan2D SunChen 
#采数
#python extra.py  ./logMTvsH18/
#python extra.py  ./log111/
#python extra.py  ../LOG46/
#python extra.py  ../LOG50/
#python extra.py  ../LOG51/ 
#python extra.py  ../LOG61/ 
#python extra.py  ../LOG63/
#python extra.py  ../LOG64/
#python extra.py  ../LOG47/
#python extra.py  ../LOG_EVA/
#python extra.py  ../LOG_EVA_NEW/
#python extra.py  ../LOG_INT_EVA/
#python extra.py  ../LOG_INT_FOR/
#python extra.py  ../log20181018评估bug/
#python extra.py  ../log20181023截球+阵型bug/
#python extra.py  ../log20181026int+npen/
#python extra.py  ../log20181031评估/
#python extra.py ../log301-442
#python extra.py ../log302-4231
#python extra.py ../log303-442
#python extra.py ../log304-442
#python extra.py ../log305-442
#python extra.py ../log306-442
#python extra.py ../log307-442
#python extra.py ../log308-442
#python extra.py ../log309-442
#python extra.py ../log段测试
#python extra.py ../log20
#python extra.py ../log22
#python extra.py ../log23
#python extra.py ../log24
#python extra.py ../log25
#python extra.py ../log310-base
#python extra.py ../log311-442v0
#python extra.py ../log312-442v1
#python extra.py ../log-db

#python extra.py ../log313-442v2
#python extra.py ../log314-442v3
#python extra.py ../log315-433v4
#python extra.py ../log316-433v5
#python extra.py ../log317-433v6
#python extra.py ../log318-433v7
#python extra.py ../log319-433v8
#python extra.py ../log-base-gld-401
#python extra.py ../log-int-402
#python extra.py ../log403-sc433
#python extra.py ../log406
#python extra.py ../log407
#python extra.py ../log408
#python extra.py ../log409
#python extra.py ../log410
#python extra.py ../log411
#python extra.py ../log603
#python extra.py ../log604
#python extra.py ./log201/
#python2 extra.py ./log1/
#python2 extra.py ../Autoplaysunc/log203/
#python2 extra.py log201
#python2 extra.py ../log
#h画图
#python3 ./result/read-histV4.py
#python3 ./result/pltBarbyDist.py
#python3 ./result/pltBarbyAngle.py
#集成
python3 ./result/togather_dist.py
python3 ./result/togather_kick.py
python3 ./result/togather_angle.py
python2 ./avg_all.py
#获得有用数据，将所有总的平局数据进行合并得到8个区域的集成文件
python3 ./lib/togather_angle_allteam_area.py
python3 ./lib/togather_dist_allteam_area.py
python3 ./lib/togather_kick_allteam_area.py

python3 ./lib/togather_angle_allteam.py
python3 ./lib/togather_dist_allteam.py
python3 ./lib/togather_kick_allteam.py

./All_Data/start.sh

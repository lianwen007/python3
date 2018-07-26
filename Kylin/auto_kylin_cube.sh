
#!/bin/bash
###################################################################################################################
## 脚本功能：之前脚本任务完成后，使用Kylin命令，增量更新Kylin cube
## 修改历史：
#            
###################################################################################################################
 
 
####之前的bi_etl脚本处理 BEGIN####
 
 
####之前的bi_etl脚本处理 END####
 
 
 
#加入Kylin增量build cube
##cubeName  cube的名称
##endTime  执行build cube的结束时间 (命令传给Kylin的kylinEndTime = realEndTime + (8小时，转化为毫秒)。只需要给Kylin传入build cube的结束时间即可。)
##buildType  BUILD 构建cube操作(还有Refresh、Merge等操作，增量构建为BUILD)
 
kylinMinusTime=$((8 * 60 * 60 * 1000)) #8小时对应的毫秒时间
tomorrow=`date -d next-day +%Y-%m-%d`
tomorrowTimeStamp=`date -d "$tomorrow 00:00:00" +%s`
tomorrowTimeStampMs=$(($tomorrowTimeStamp*1000 + `date "+%N"`/1000000)) #将current转换为时间戳，精确到毫秒
endTime=$(($tomorrowTimeStampMs + $kylinMinusTime))
 
cubeName=saiku_kylin_cube2
 
curl -X PUT -H "Authorization: Basic QURNSU46S1lMSU4=" -H 'Content-Type: application/json' -d '{"endTime":'$endTime', "buildType":"BUILD"}' http://192.168.23.235:7070/kylin/api/cubes/$cubeName/rebuild

import pandas as pd

#筛选A列名字里面包括刘，且B列年龄大于60的，则更新数据D列的内容为1。不符合条件的行，D列数据不变

rs = pd.DataFrame({'A':['我b45D','刘245D','刘123','刘123'],
                  'B':[20,30,60,80],
                    'D':[0,3,5,2]})
                 
rs['D'][(rs['A'].str.contains('刘')) & (rs['B']>=60)] = 1  


# dict or list 转换为 dataframe
tdata = [
    {
      "taskFixNum": 12, 
      "taskStuNum": 600, 
      "taskUploadNum": 50, 
      "tchId": 70155
    }, 
    {
      "taskFixNum": 12, 
      "taskStuNum": 588, 
      "taskUploadNum": 50, 
      "tchId": 70155
    }]
trs = pd.DataFrame(tdata)

dict_country = trs.to_json(orient='records')  

# dataframe 转 json
import json
inp_dict = json.loads(dict_country)

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 10:04:09 2018

@author: Administrator
"""

import sys
import ast


for v in sys.stdin:  # json使用‘@’分割，HIVE可正确解析
    if v:
        value = v.replace('"[',"[").replace(']"',']').replace('false','0').replace('true','1').replace('\\','')
        try:
            results = ast.literal_eval(value)
        except:
            continue
        all_mess = ''
        if results:
            if type(results) == type(list()):
                for x in results:
                    all_mess = all_mess + str(x) + '@' 
                print (all_mess.rstrip('@'))
            elif type(results) == type(dict()):
                for x in results:
                    d = dict()
                    if type(results[x]) == type(list()):  # 判断是否为list，是则处理，否则直接输出
                        in_list = ''
                        for y in results[x]:  # json内部list内的dict使用‘#’分割
                            in_list = in_list + str(y) + '#'
                        d[x] = in_list.rstrip('#')
                    else:
                        d[x] = results[x]
                    all_mess = all_mess + str(d) + '@'
                print (all_mess.rstrip('@'))
            else:
                print(all_mess)
        else:
            continue
    else:
        continue

#
#a = '''
#[{"answerType":2,"bookId":"5ab061b4363d7824cacdaf08","catalogId":"5ab061b4363d7824cacdaf0e","collect":0,"crossheadCount":10,"crossheadRight":9,"difficulty":0,"isContinuity":false,"isSurprise":false,"questionId":"5aaf7e0f363d7824cacd92a5","questionType":0,"right":2,"score":9.0,"studentAnswer":"[]","type":9,"userType":9},{"answerType":2,"bookId":"5ab061b4363d7824cacdaf08","catalogId":"5ab061b4363d7824cacdaf0e","collect":0,"crossheadCount":10,"crossheadRight":0,"difficulty":0,"isContinuity":false,"isSurprise":false,"parentQuestionId":"5aaf7e0f363d7824cacd92a5","questionId":"5aaf7e0a376df96fec22c0dc","questionType":0,"right":0,"score":0.0,"studentAnswer":"[{\"stuReply\":\"b\",\"index\":0,\"inputType\":2,\"isRepeatRevise\":false,\"isSeekHelp\":false,\"isShowAnswerImg\":false,\"isShowProofreadRed\":true,\"isTchRepeatRevise\":false,\"proofreadResult\":1,\"sectionIndex\":-1,\"sectionProofreadResult\":-1}]","type":4,"userType":0}]
#'''
#
#value = a.replace('"[',"[").replace(']"',']').replace('false','0').replace('true','1').replace('\\','')
#try:
#    results = ast.literal_eval(value)
#except:
#    results = dict()
#all_mess = ''
#if results:
#    if type(results) == type(list()):
#        for x in results:
#            all_mess = all_mess + str(x) + '@' 
#        print (all_mess.rstrip('@'))
#    else:
#        for x in results:
#            d = dict()
#            d[x] = results[x]
#            all_mess = all_mess + str(d) + '@' 
#        print (all_mess.rstrip('@')) 

#
#
#import sys
#import ast
for v in sys.stdin:
    if v:
        value = v.replace('"[',"[").replace(']"',']').replace('false','0').replace('true','1').replace('\\','')
        try:
            results = ast.literal_eval(value)
        except:
            continue
        all_mess = ''
        if results:
            if type(results) == type(list()):
                for x in results:
                    all_mess = all_mess + str(x) + '@' 
                print (all_mess.rstrip('@'))
            elif type(results) == type(dict()):
                for x in results:
                    d = dict()
                    d[x] = results[x]
                    all_mess = all_mess + str(d) + '@' 
                print (all_mess.rstrip('@'))
            else:
                print(all_mess)
        else:
            continue
    else:
        continue
#
#
#
#import sys
#import ast
#
#for values in sys.stdin:
#    if values:
#        value = values.replace('"[',"[").replace(']"',']').replace('false','0').replace('true','1').replace('\\','')
#        try:
#            result = ast.literal_eval(value)
#        except:
#            result = tuple()
#        print (str(len(result)))
#    else:
#        pass
    
s = '{a: 1, b: 2}'

#for line in sys.stdin:  
#    detail = line.strip().split('\t')
#    if (len(detail) < 4):  
#        continue  
#    mid = detail[0]  
#    pid = detail[1]  
#    trans_at = detail[2]  
#    total_cnt = detail[3]  
#  
#    trans_at_month = trans_at.split(',')  
#    if (len(trans_at_month) != 12):  
#        continue  
#    flag = True  
#    for money in trans_at_month:  
#        if (float(money) < 10000.0):  
#            flag = False  
#    if (flag):  
#    print ('%s\t%s\t%s\t%s' % (mid, pid, trans_at, total_cnt))

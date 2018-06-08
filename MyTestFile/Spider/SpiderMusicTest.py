# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 15:59:07 2018

@author: Administrator
"""




import requests
import json

#爬取陈奕迅的《我们》的热门评论
#参数：url,headers,user_data(params,encSecKey)
url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_551816010?csrf_token='    #评论所在的链接
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Referer':'http://music.163.com/song?id=551816010',
    'Origin':'http://music.163.com',
    'Host':'music.163.com'
}
#加密数据，直接拿过来用
user_data = {
    'params':'60e75d03+rb9U8IQhy6/9+H1si5pp7qLysZoQsYG9qFkXtXL9dRKMfchCKpJ8OpN9m7vSRVkYWN+wscyUqelunqxGDozt2bJWQ2QRj4pJrSa0xoJPAk5Jw8t70rYW8hwdyoYswl+kRQTQ6oz3eHHZ5BLzZZB4t/4asFSQQDnCteg2GqrEJBomMgpFMIa4Ybt',
    'encSecKey':'52db8824c86503bc2cfc050ac78969c9155ff08f274f88b767ad6535febcbad021d0cdabcc172e01f91c42a2aca0786e407935f8feaa44a03efb96ec9d71de181e92ae8471738e4a43b252f22b46739cb3b86544a9f9403b0402bd9638a3bc2b87bf3a0b9cff6ef7b6b1589f00a5bfeecb9d45c493456082d80fbece6ac5a3fa'
}

response = requests.post(url,headers=headers,data=user_data)
data = json.loads(response.text)
hotcomments = []
for hotcomment in data['hotComments']:
    item = {
        'nickname':hotcomment['user']['nickname'],
        'content':hotcomment['content'],
        'likedCount':hotcomment['likedCount']
    }
    hotcomments.append(item)
#获取评论用户名，内容，以及对应的获赞数
content_list = [content['content'] for content in hotcomments]
nickname = [content['nickname'] for content in hotcomments]
liked_count = [content['likedCount'] for content in hotcomments]

#点赞数
from pyecharts import Bar      #pyecharts：图表包
bar = Bar('热门中点赞数示例图')
bar.add('点赞数',nickname,liked_count,is_stack=True,mark_line=['min','max'],mark_point=['average'])
bar.render()

#词云图
from wordcloud import WordCloud     #WordCloud：词云包
import matplotlib.pyplot as plt     #matplotlib：绘图功能包
content_text = ' '.join(content_list)
wordcloud = WordCloud(font_path=r'C:\simhei.ttf',max_words=200).generate(content_text)
plt.figure()
plt.imshow(wordcloud,interpolation='bilinear')
plt.axis('off')
plt.show()

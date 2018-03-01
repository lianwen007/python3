# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 16:45:29 2018

@author: Administrator
"""

import requests
import json

#def post_some_dict(dict):
#    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
#    r = requests.post(url, data=json.dumps(dict), headers=headers)
#    
#data = {"somekey": 12}
headers = {"Content-type": "application/json", "Accept": "text/plain"}
#conn = httplib.HTTPConnection('xx.xx.xx.xx')
#conn.request("POST", "/", json.dumps(data), headers)


url = 'http://bigdata.yunzuoye.net/bigdata/product_stw/getstwinfo'
s = json.dumps({
  "schoolid": "4114",
  "bookid": "5a698ec0363d78315d2e49c8"
})
r = requests.post(url, data=s, headers=headers)
print (r.text + str(r.status_code))

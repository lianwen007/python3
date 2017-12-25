from datetime import datetime
from elasticsearch import Elasticsearch
import json
from elasticsearch import helpers


es=Elasticsearch(['192.168.5.57'],port=9200)
set_search={"query": {
            "match": {"local_addr":"ztp.yunzuoye.net"}
        }
}

ressearch = helpers.scan(es,set_search, scroll= "10m", index="nginx-2017.10.14", doc_type="nginx", timeout="10m")

for a,b in ressearch.items():
	if a=='_source':
		for c,d in b.items():
			if c=='message' or c=='local_addr' or c=='request' or c=='time_local':
				mess=d
				jsObj = json.dumps(mess)
				fileObject = open('jsonFile1.json', 'a')
				fileObject.write(jsObj+',\n')
# 限定条件下ELK取出至TXT文件。

'''
for res in ressearch:
    jsObj = json.dumps(res["_source"])
    # jsObj = json.loads(res)
    fileObject = open('jsonFile3.json', 'a')
    fileObject.write(jsObj+',\n')


for a,b in messages.items():
	if a=='_source':
		for c,d in b.items():
			if c=='message' or c=='local_addr' or c=='request' or c=='time_local':
				mess=d
'''

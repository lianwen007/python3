import pyhs2

with pyhs2.connect(host='192.168.0.0',port=6666,authMechanism="NOSASL",user='',password='*',database='default') as conn:
    with conn.cursor() as cur:
        print (cur.getDatabases())
        cur.execute("select * from xhschool_info")
        #Return column info from query
        print (cur.getSchema())
        #Fetch table results
        for i in cur.fetch():
            print (i)

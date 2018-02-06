## API desc
#####  <p id="getstwinfo">getstwinfo</p>
#####  <p id="jsontocsv">jsontocsv</p>
#####  <p id="getuserinfo">UserLogon</p>

#### "/bigdata/product_stw/getstwinfo"<a name="#getstwinfo"></a> 
```
POST:
{
"schoolid":"3495,760",
"starttime":1517328000,
"endedtime":1517534599
}

RETURN:
{ 
"code": int,
"msg": "string",
"data":'[ json ]'
}
```

#### "/bigdata/product_stw/jsontocsv"<a name="#jsontocsv"></a> 
```
POST:
{
form-data(
    key:stwdata ,
    value:str[ json ]
    )
}
```
#### "/bigdata/getuserinfo"<a name="#getuserinfo"></a>
```
POST:
{
    "username":"string",
    "password":"MD5-string"
}
RETURN:
{
    "userid": int,
    "logonName": "string",
    "userType": int,
    "userPhone": int,
}

## API desc
#####  <p id="getstwinfo">getstwinfo</p>
#####  <p id="jsontocsv">jsontocsv</p>

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
"msg": string,
"data":[ json ]
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

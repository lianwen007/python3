# API For Product

### app.getEnStwInfo - 英语刷题王3统计接口 API for count info of Englishking3
### app.getKpiInfo - 考核统计信息接口 API for count info of kpis
### app.getStwInfo - 刷题王3统计信息接口 API for count info of king3 
</br>

#### Update Info app.getStwInfo:
##### **2018-04-02**
> * 加入缓存清除，接口调取可清除历史缓存
> * 内部调取学科信息接口
> * 增加判定，只返回学科下所有教师

##### **2018-03-28**
> * 增加SubTpye判定，不同规则执行不同算法
> * 空数据BUG修复，正确返回

##### **2018-03-26**
> * 输出增加所有学生信息，无数据输出为0
> * 增加错误入参判定与报错
> * 班级所有学生信息提取加入缓存机制，过期时间12小时

##### **2018-03-22**
> * 学生信息接口更新，入参修改 `SubID` 为 `SubjectName`
> * 新增获取学生基础信息统计接口。METHOD方法判定
> * 实时数据接口重构，加入缓存机制过期时间50分钟

##### **2018-03-15**
> * 增加全量数据，接口调取时的内部计算，优化处理速度
> * 日志结构变更，规范标题大小写

##### **2018-03-07**
> * 增加HP等字段的实时调用接口 


#### Update Info app.getEnStwInfo:
##### **2018-04-02**
> * 新增英刷数据接口
> * 学生信息获取全部，无数据填充0

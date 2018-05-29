
# java
package com;
public class Test {
    public String run(String str){
        return str;
    }
}

"""
// 编译
javac Test.java

// 打包，必须把整个目录（报名和目录名要对应）打包，否则无法访问类。
jar cvf test.jar com
"""

# python
import jpype 
import os
jarpath = os.path.join(os.path.abspath('.'), 'test.jar')
jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % jarpath)
Test = jpype.JClass('com.Test')
# 或者通过JPackage引用Test类
# com = jpype.JPackage('com')
# Test = com.Test
t = Test()
res = t.run("a")
print (res)
jpype.shutdownJVM()

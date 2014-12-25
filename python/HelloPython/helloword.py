#__author__ = 'zhangyi'
from HelloPython import hellomodule

print 'hello world'
print hellomodule.word


num="";
for i in range(1,1025):
    num+=str(i)
print num
print int(num)%9
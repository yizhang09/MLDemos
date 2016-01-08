#!/usr/bin/env python
# -- coding: utf-8 --


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import Series,DataFrame
from matplotlib.font_manager import FontProperties

font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)

data_train = pd.read_csv("data/train.csv")
data_train.info()
#data_train.describe()

fig = plt.figure()
fig.set(alpha=0.2) #设定图表颜色alpha参数

plt.subplot2grid((2,3),(0,0))
data_train.Survived.value_counts().plot(kind='bar')
plt.title(u"获救情况（1为获救）",fontproperties = font)
plt.ylabel(u"人数",fontproperties = font)

plt.subplot2grid((2,3),(0,1))
data_train.Pclass.value_counts().plot(kind='bar')
plt.title(u"乘客等级情况",fontproperties = font)
plt.ylabel(u"人数",fontproperties = font)

plt.subplot2grid((2,3),(0,2))
plt.scatter(data_train.Survived,data_train.Age)
plt.grid(b=True,which='major',axis='y')
plt.ylabel(u"年龄",fontproperties = font)

plt.subplot2grid((2,3),(1,0), colspan=2)
data_train.Age[data_train.Pclass == 1].plot(kind='kde')
data_train.Age[data_train.Pclass == 2].plot(kind='kde')
data_train.Age[data_train.Pclass == 3].plot(kind='kde')
plt.xlabel(u"年龄",fontproperties = font)
plt.ylabel(u"密度",fontproperties = font)
plt.title(u"各等级乘客年龄分布",fontproperties = font)
plt.legend((u"1等舱",u"2等舱",u"3等舱"),loc='best')

plt.subplot2grid((2,3),(1,2))
data_train.Embarked.value_counts().plot(kind='bar')
plt.title(u"各登船口岸上船人数",fontproperties = font)
plt.ylabel(u"人数",fontproperties = font)


Survived_0 = data_train.Pclass[data_train.Survived == 0].value_counts()
Survived_1 = data_train.Pclass[data_train.Survived == 1].value_counts()
df=pd.DataFrame({u'获救':Survived_1, u'未获救':Survived_0})
df.plot(kind='bar', stacked=True)
plt.title(u"各乘客等级的获救情况",fontproperties = font)
plt.xlabel(u"乘客等级",fontproperties = font)
plt.ylabel(u"人数",fontproperties = font)


plt.show()




#!/usr/bin/env python
# -- coding: utf-8 --


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import Series,DataFrame
from matplotlib.font_manager import FontProperties

from sklearn.ensemble import RandomForestRegressor
import sklearn.preprocessing as pp
from sklearn import linear_model


data_train = pd.read_csv("data/train.csv")
data_train.info()
data_train.describe()


def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')


def data_analysis():
    font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
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


def set_missing_ages(df):
    #预测年龄，将NaN值改为预测值 使用随机森林算法
    age_df = df[['Age','Fare','Parch','SibSp','Pclass']]
    known_df = age_df[age_df.Age.notnull()].as_matrix()
    unknown_df = age_df[age_df.Age.isnull()].as_matrix()

    y = known_df[:,0]
    X = known_df[:,1:]

    rfr = RandomForestRegressor(random_state=0,n_estimators=2000,n_jobs=-1)
    rfr.fit(X,y)
    predict_age = rfr.predict(unknown_df[:,1::])
    df.loc[(df.Age.isnull()),'Age'] = predict_age

    return df,rfr

def set_Cabin_Type(df):
    #处理仓位
    df.loc[(df.Cabin.notnull()),'Cabin'] = "Yes"
    df.loc[(df.Cabin.isnull()),'Cabin'] = "No"
    return df

def dummy_data(df):
    #特征因子化，将性别男、女，改成是否男性、是否女性这样的多列是否值
    dummies_Cabin = pd.get_dummies(df['Cabin'],prefix='Cabin')
    dummies_Embarked = pd.get_dummies(df['Embarked'],prefix='EmBarked')
    dummies_Sex = pd.get_dummies(df['Sex'],prefix='Sex')
    dummies_Pclass = pd.get_dummies(df['Pclass'],prefix='Pclass')
    df = pd.concat([df,dummies_Cabin,dummies_Embarked,dummies_Sex,dummies_Pclass],axis=1)
    df.drop(['Pclass','Name','Sex','Ticket','Cabin','Embarked'],axis=1,inplace=True)
    return df

def scale_data(df):
    scaler = pp.StandardScaler()
    age_scaler_param = scaler.fit(df['Age'])
    df['Age_scaled'] = scaler.fit_transform(df['Age'],age_scaler_param)
    fare_scaler_param = scaler.fit(df['Fare'])
    df['Fare_scaled'] = scaler.fit_transform(df['Fare'],fare_scaler_param)
    return df

def buildmodel(df):
    train_df = df.filter(regex='Survived|Age_.*|SibSp|Parch|Fare_.*|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*')
    train_np = train_df.as_matrix()
    y = train_np[:,0]
    X = train_np[:,1:]
    clf = linear_model.LogisticRegression(C=1.0,penalty='l1',tol=1e-6)
    clf.fit(X,y)
    print 'OK'
    return clf



data_train,rfr = set_missing_ages(data_train)
data_train = set_Cabin_Type(data_train)
data_train = dummy_data(data_train)
data_train = scale_data(data_train)

data_test = pd.read_csv("data/test.csv")
data_test.loc[ (data_test.Fare.isnull()), 'Fare' ] = 0
# 接着我们对test_data做和train_data中一致的特征变换
# 首先用同样的RandomForestRegressor模型填上丢失的年龄
# 根据特征属性X预测年龄并补上
data_test,rfr = set_missing_ages(data_test)
data_test = set_Cabin_Type(data_test)
data_test = dummy_data(data_test)
data_test = scale_data(data_test)

clf = buildmodel(data_train)

test = data_test.filter(regex='Age_.*|SibSp|Parch|Fare_.*|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*')
predictions = clf.predict(test)
result = pd.DataFrame({'PassengerId':data_test['PassengerId'].as_matrix(),'Survived':predictions.astype(np.int32)})
result.to_csv('data/result.csv',index=False)


#print_full(data_train)
print data_train




